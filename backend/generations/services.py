import os
import json
import logging
from PIL import Image, ImageOps
from urllib.parse import urlparse
from datetime import timedelta
from io import BytesIO
from django.conf import settings
from django.db import transaction, connections
from django.utils import timezone
from django.utils.text import slugify
from .models import GenerationRequest
from subscriptions.models import UserSubscription
from tenacity import retry, wait_random_exponential, retry_if_exception, stop_after_delay
from gcloud.aio.storage import Storage as GCSAsyncStorage
from google.cloud import storage as gcs_sync_storage
from asgiref.sync import sync_to_async
from google import genai
from google.genai import types
from google.cloud.tasks_v2.types import HttpMethod
from google.genai.types import HarmCategory, HarmBlockThreshold
from google.genai import errors
from generations.views import tasks_client

logger = logging.getLogger(__name__)
gcs_sync_storage_client = gcs_sync_storage.Client()

class ContentBlockedError(Exception):
    pass

def is_retryable_error(error):
    if isinstance(error, errors.ServerError):
        return True
        
    if isinstance(error, errors.ClientError) and hasattr(error, 'code') and error.code == 429:
        return True
    return False

@retry(wait=wait_random_exponential(min=5, max=60), stop=stop_after_delay(240), retry=retry_if_exception(is_retryable_error))
async def generate_output_image(prompt, input_image_bytes):
    image = Image.open(BytesIO(input_image_bytes))
    genai_client = genai.Client()

    try:
        response = await genai_client.aio.models.generate_content(
            model="gemini-2.5-flash-image",
            contents = [prompt, image],
            config=types.GenerateContentConfig(
                safety_settings=[
                    {
                        "category": HarmCategory.HARM_CATEGORY_HARASSMENT,
                        "threshold": HarmBlockThreshold.BLOCK_NONE
                    },
                    {
                        "category": HarmCategory.HARM_CATEGORY_HATE_SPEECH,
                        "threshold": HarmBlockThreshold.BLOCK_NONE
                    },
                    {
                        "category": HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT,
                        "threshold": HarmBlockThreshold.BLOCK_NONE
                    },
                    {
                        "category": HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
                        "threshold": HarmBlockThreshold.BLOCK_NONE
                    }
                ]
            )
        )
    
        if not response.candidates[0].content:
            raise ContentBlockedError()

        output_image_bytes = None
        
        for part in response.candidates[0].content.parts:
            if part.inline_data:
                output_image_bytes = part.inline_data.data
                break

        return output_image_bytes
    finally:
        if genai_client._api_client._aiohttp_session:
            await genai_client._api_client._aiohttp_session.close()



def delete_generation_request_images_from_gcs(generation_request):
    urls_to_delete = [
        generation_request.input_img_url,
        generation_request.output_img_url
    ]
    bucket_name = settings.GCP_STORAGE_BUCKET_NAME
    bucket = gcs_sync_storage_client.bucket(bucket_name)

    for url in urls_to_delete:
        if not url:
            continue
        
        path = urlparse(url).path.lstrip('/')
        _, blob_name = path.split('/', 1)
        
        base_name, _ = os.path.splitext(blob_name)
        thumbnail_blob_name = f"{base_name}_200x200.webp"

        original_blob = bucket.blob(blob_name)
        thumbnail_blob = bucket.blob(thumbnail_blob_name)

        if original_blob.exists() and thumbnail_blob.exists():
            original_blob.delete()
            thumbnail_blob.delete()
        else:
            logger.error(f"Missing original or thumbnail blob in deletion request", extra={'original_blob_name': blob_name, 'thumbnail_blob_name': thumbnail_blob_name})

def upload_output_image_to_gcs(image_bytes, user_id, style_name):
    slugified_style_name = slugify(style_name)
    timestamp = timezone.now().strftime('%Y-%m-%d-%H-%M-%S')

    content_type = 'image/png'
    file_extension = 'png'

    bucket_name = settings.GCP_TEMP_BUCKET_NAME
    blob_name = f"users/{user_id}/outputs/{slugified_style_name}-{timestamp}.{file_extension}"

    bucket = gcs_sync_storage_client.bucket(bucket_name)
    blob = bucket.blob(blob_name)

    blob.upload_from_string(image_bytes, content_type=content_type)

    return f"https://storage.googleapis.com/{bucket_name}/{blob_name}"



def create_task_for_resizing(generation_request_id, user_id, input_img_url, output_img_url=None):
    try:
        target_url = settings.RESIZING_WORKER_URL
        
        event_data = {
            "generation_request_id": generation_request_id,
            "user_id": str(user_id),
            "input_img_url": input_img_url,
            "output_img_url": output_img_url
        }

        queue_path = tasks_client.queue_path(
            settings.GCP_PROJECT_ID,
            settings.GCP_TASKS_LOCATION,
            settings.GCP_TASKS_RESIZE_QUEUE_ID,
        )

        task = {
            'http_request': {
                'url': target_url,
                'http_method': HttpMethod.POST,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps(event_data).encode('utf-8'),
            },
        }

        tasks_client.create_task(request={'parent': queue_path, 'task': task})
    except Exception as e:
        logger.error(f"Failed to create resizing task for generation request", extra={'generation_request_id': generation_request_id, 'error': str(e)}, exc_info=True)
        raise

@sync_to_async
def processing_successful_generation(generation_request_id, output_image_bytes, user_id, style_name):
    with transaction.atomic():
        try:
            generation_request = GenerationRequest.objects.select_for_update().get(id=generation_request_id)
        except GenerationRequest.DoesNotExist:
            logger.error(f"Generation request was deleted. Upload and processing aborted", extra={'generation_request_id': generation_request_id})
            return
        
        output_img_url = upload_output_image_to_gcs(
            image_bytes=output_image_bytes,
            user_id=user_id,
            style_name=style_name
        )

        subscription_for_debiting_credit = generation_request.user.subscriptions.select_for_update().filter(
            status=UserSubscription.SubscriptionStatus.ACTIVE,
            remaining_credits__gt=0
        ).order_by('end_time').first()
        
        if not subscription_for_debiting_credit:
            generation_request.output_img_url = output_img_url
            generation_request.status = GenerationRequest.GenerationStatus.COMPLETED
            generation_request.error_message = "Credit was not debited: no active subscription with credits at processing time"
            generation_request.save(update_fields=['output_img_url', 'status', 'error_message', 'updated_at'])
            logger.error(f"Credit not debited, no active subscription found", extra={'generation_request_id': generation_request.id})
            return

        subscription_for_debiting_credit.remaining_credits -= 1
        subscription_for_debiting_credit.save(update_fields=['remaining_credits'])

        generation_request.output_img_url = output_img_url
        generation_request.status = GenerationRequest.GenerationStatus.COMPLETED
        generation_request.save(update_fields=['output_img_url', 'status', 'updated_at'])

        transaction.on_commit(lambda: create_task_for_resizing(
            generation_request_id=generation_request_id,
            user_id=user_id,
            input_img_url=generation_request.input_img_url,
            output_img_url=output_img_url
        ))

async def handle_generation_process(generation_request_id):
    try:
        generation_request = await GenerationRequest.objects.select_related('user', 'chosen_style').aget(id=generation_request_id)
    except GenerationRequest.DoesNotExist:
        return
    except Exception as e:
        logger.error(f"Failed to get generation request", extra={'generation_request_id': generation_request_id, 'error': str(e)}, exc_info=True)
        return
    
    try:
        if not all([
            generation_request.input_img_url,
            generation_request.chosen_style,
            generation_request.chosen_style.prompt_template,
            generation_request.chosen_style.name,
            generation_request.user
        ]):
            raise Exception("Input data is missing")
        
        prompt = generation_request.chosen_style.prompt_template
        style_name = generation_request.chosen_style.name
        input_image_url = generation_request.input_img_url
        user_id = generation_request.user.id

        parsed_url = urlparse(input_image_url)
        path = parsed_url.path.lstrip('/')

        if '/' not in path:
            raise Exception("Failed to parse GCS URL path: URL path does not contain a separator")

        bucket_name, blob_name = path.split('/', 1)

        if not bucket_name or not blob_name:
            raise Exception("Failed to parse GCS URL path: bucket name or blob name is empty after split")

        async with GCSAsyncStorage() as gcs_async_storage_client:
            input_image_bytes = await gcs_async_storage_client.download(bucket_name, blob_name)
    
        await sync_to_async(connections.close_all)()
        output_image_bytes = await generate_output_image(prompt, input_image_bytes)

        if not output_image_bytes:
            raise Exception("Generated image data is empty")

        await processing_successful_generation(generation_request_id, output_image_bytes, user_id, style_name)
    except ContentBlockedError:
        try:
            await sync_to_async(delete_generation_request_images_from_gcs)(generation_request)
        except Exception as e:
            logger.error(f"Failed to delete generation request images from GCS after rejection by safety system", extra={'generation_request_id': generation_request_id, 'error': str(e)}, exc_info=True)

        generation_request.input_img_url = None
        generation_request.status = GenerationRequest.GenerationStatus.REJECTED_BY_SAFETY
        generation_request.error_message = "Request was rejected by the safety system"
        await generation_request.asave(update_fields=['input_img_url', 'status', 'error_message', 'updated_at'])
    except Exception as e:
        logger.error(f"Error during image generation process", extra={'generation_request_id': generation_request_id, 'error': str(e)}, exc_info=True)

        generation_request.status = GenerationRequest.GenerationStatus.FAILED
        generation_request.error_message = str(e)
        await generation_request.asave(update_fields=['status', 'error_message', 'updated_at'])

        sync_to_async(create_task_for_resizing)(generation_request_id, user_id, input_image_url)



def upload_input_image_to_gcs(image_file, user_id):
    image_file.seek(0)

    image = Image.open(image_file)
    image = ImageOps.exif_transpose(image)

    buffer = BytesIO()
    image.save(buffer, format=image.format)

    content_type = Image.MIME.get(image.format)
    file_extension = f"{image.format.lower().replace('jpeg', 'jpg')}"

    timestamp = timezone.now().strftime('%Y-%m-%d-%H-%M-%S')
    bucket_name = settings.GCP_TEMP_BUCKET_NAME
    blob_name = f"users/{user_id}/inputs/input-{timestamp}.{file_extension}"
    
    bucket = gcs_sync_storage_client.bucket(bucket_name)
    blob = bucket.blob(blob_name)
    
    blob.upload_from_string(buffer.getvalue(), content_type=content_type)

    return f"https://storage.googleapis.com/{bucket_name}/{blob_name}"

def generate_signed_gcs_url(gcs_img_url, expires_in_seconds, response_disposition=None):
    parsed_url = urlparse(gcs_img_url)
    path = parsed_url.path.lstrip('/')
    bucket_name, blob_name = path.split('/', 1)

    bucket = gcs_sync_storage_client.bucket(bucket_name)
    blob = bucket.blob(blob_name)

    return blob.generate_signed_url(
        expiration=timedelta(seconds=expires_in_seconds),
        version='v4',
        method='GET',
        response_disposition=response_disposition
    )

def get_user_gcs_all_blob_names(user_id):
    bucket_name = settings.GCP_STORAGE_BUCKET_NAME
    bucket = gcs_sync_storage_client.bucket(bucket_name)
    prefix = f"users/{user_id}/"
    blobs = bucket.list_blobs(prefix=prefix)
    
    return [blob.name for blob in blobs]