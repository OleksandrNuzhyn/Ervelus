import os
import logging
from PIL import Image, ImageOps
from urllib.parse import urlparse
from datetime import timedelta
from io import BytesIO
from django.conf import settings
from django.db import transaction, close_old_connections
from django.utils import timezone
from django.utils.text import slugify
from .models import GenerationRequest
from subscriptions.models import UserSubscription
from tenacity import retry, wait_random_exponential, retry_if_exception, stop_after_attempt
from gcloud.aio.storage import Storage as GCSAsyncStorage
from google.cloud import storage as gcs_sync_storage
from asgiref.sync import sync_to_async
from google import genai
from google.genai import types
from google.genai.types import HarmCategory, HarmBlockThreshold
from google.genai import errors

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

@retry(wait=wait_random_exponential(min=5, max=60), stop=stop_after_attempt(7), retry=retry_if_exception(is_retryable_error))
async def generate_output_image(prompt, input_image_bytes):
    image = Image.open(BytesIO(input_image_bytes))
    genai_client = genai.Client()

    try:
        response = await genai_client.aio.models.generate_content(
            model="gemini-2.5-flash-image-preview",
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

async def upload_output_image_to_gcs(image_bytes, user_id, style_name):
    prepared_image_bytes = await sync_to_async(prepare_image_for_upload)(image_bytes, quality=100)

    slugified_style_name = slugify(style_name)
    timestamp = timezone.now().strftime('%Y-%m-%d-%H-%M-%S')

    bucket_name = settings.GCP_STORAGE_BUCKET_NAME
    blob_name = f"users/{user_id}/images/outputs/{slugified_style_name}-{timestamp}.jpg"

    async with GCSAsyncStorage() as gcs_async_storage_client:
        await gcs_async_storage_client.upload(bucket_name, blob_name, prepared_image_bytes, content_type='image/jpeg')

    return f"https://storage.googleapis.com/{bucket_name}/{blob_name}"



@sync_to_async
def processing_successful_generation(generation_request, output_image_url):
    with transaction.atomic():
        subscription_for_debiting_credit = generation_request.user.subscriptions.select_for_update().filter(
            status=UserSubscription.SubscriptionStatus.ACTIVE,
            remaining_credits__gt=0
        ).order_by('end_time').first()
        
        if not subscription_for_debiting_credit:
            generation_request.output_img_url = output_image_url
            generation_request.status = GenerationRequest.GenerationStatus.COMPLETED
            generation_request.error_message = "Credit was not debited: no active subscription with credits at processing time"
            generation_request.save(update_fields=['output_img_url', 'status', 'error_message', 'updated_at'])
            logger.error(f"Credit not debited, no active subscription found", extra={'generation_request_id': generation_request.id})
            return

        subscription_for_debiting_credit.remaining_credits -= 1
        subscription_for_debiting_credit.save(update_fields=['remaining_credits'])

        generation_request.output_img_url = output_image_url
        generation_request.status = GenerationRequest.GenerationStatus.COMPLETED
        generation_request.save(update_fields=['output_img_url', 'status', 'updated_at'])

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
            generation_request.status = GenerationRequest.GenerationStatus.FAILED
            generation_request.error_message = "Input data is missing"
            await generation_request.asave(update_fields=['status', 'error_message', 'updated_at'])
            logger.error(f"Input data is missing", extra={'generation_request_id': generation_request_id})
            return
    except Exception as e:
        logger.error(f"Failed to check input data", extra={'generation_request_id': generation_request_id, 'error': str(e)}, exc_info=True)
        return
    
    prompt = generation_request.chosen_style.prompt_template
    style_name = generation_request.chosen_style.name
    input_image_url = generation_request.input_img_url
    user_id = generation_request.user.id

    try:
        parsed_url = urlparse(input_image_url)
        path = parsed_url.path.lstrip('/')

        if '/' not in path:
            raise ValueError("URL path does not contain a separator")

        bucket_name, blob_name = path.split('/', 1)

        if not bucket_name or not blob_name:
            raise ValueError("Bucket name or blob name is empty after split")
    except ValueError as e:
        logger.error(f"Failed to parse GCS URL path", extra={'generation_request_id': generation_request_id, 'error': str(e)})

        generation_request.status = GenerationRequest.GenerationStatus.FAILED
        generation_request.error_message = "Failed to parse GCS URL path"
        await generation_request.asave(update_fields=['status', 'error_message', 'updated_at'])
        return

    try:
        async with GCSAsyncStorage() as gcs_async_storage_client:
            input_image_bytes = await gcs_async_storage_client.download(bucket_name, blob_name)
    except Exception as e:
        logger.error(f"Failed to download input image from GCS", extra={'generation_request_id': generation_request_id, 'error': str(e)}, exc_info=True)

        try:
            await sync_to_async(generation_request.refresh_from_db)()
        except GenerationRequest.DoesNotExist:
            return

        if generation_request.status == GenerationRequest.GenerationStatus.STOPPED_BY_USER:
            return

        generation_request.status = GenerationRequest.GenerationStatus.FAILED
        generation_request.error_message = "Failed to download input image from GCS"
        await generation_request.asave(update_fields=['status', 'error_message', 'updated_at'])
        return

    try:        
        close_old_connections()
        output_image_bytes = await generate_output_image(prompt, input_image_bytes)

        if not output_image_bytes:
            raise ValueError("Generated image data is empty")
    except ContentBlockedError:
        try:
            await sync_to_async(generation_request.refresh_from_db)()
        except GenerationRequest.DoesNotExist:
            return

        if generation_request.status == GenerationRequest.GenerationStatus.STOPPED_BY_USER:
            logger.error(f"Generation request stopped by user with content blocked error", extra={'generation_request_id': generation_request_id})
            return

        try:
            await sync_to_async(delete_generation_request_images_from_gcs)(generation_request)
        except Exception as e:
            logger.error(f"Failed to delete generation request images from GCS after rejection by safety system", extra={'generation_request_id': generation_request_id, 'error': str(e)}, exc_info=True)

        generation_request.input_img_url = None
        generation_request.status = GenerationRequest.GenerationStatus.REJECTED_BY_SAFETY
        generation_request.error_api_message = "Your request was rejected by the safety system"
        await generation_request.asave(update_fields=['input_img_url', 'status', 'error_api_message', 'updated_at'])
        return
    except Exception as e:
        logger.error(f"Failed to generate output image", extra={'generation_request_id': generation_request_id, 'error': str(e)}, exc_info=True)
        
        try:
            await sync_to_async(generation_request.refresh_from_db)()
        except GenerationRequest.DoesNotExist:
            return

        if generation_request.status == GenerationRequest.GenerationStatus.STOPPED_BY_USER:
            return

        generation_request.status = GenerationRequest.GenerationStatus.FAILED
        generation_request.error_api_message = "Failed to generate output image"
        await generation_request.asave(update_fields=['status', 'error_api_message', 'updated_at'])
        return

    try:
        try:
            await sync_to_async(generation_request.refresh_from_db)()
        except GenerationRequest.DoesNotExist:
            return

        if generation_request.status == GenerationRequest.GenerationStatus.STOPPED_BY_USER:
            return

        output_image_url = await upload_output_image_to_gcs(
            image_bytes=output_image_bytes,
            user_id=user_id,
            style_name=style_name
        )
    except Exception as e:
        logger.error(f"Failed to upload output image to GCS", extra={'generation_request_id': generation_request_id, 'error': str(e)}, exc_info=True)

        try:
            await sync_to_async(generation_request.refresh_from_db)()
        except GenerationRequest.DoesNotExist:
            return

        if generation_request.status == GenerationRequest.GenerationStatus.STOPPED_BY_USER:
            return

        generation_request.status = GenerationRequest.GenerationStatus.FAILED
        generation_request.error_message = "Failed to upload output image to GCS"
        await generation_request.asave(update_fields=['status', 'error_message', 'updated_at'])
        return

    try:
        await processing_successful_generation(generation_request, output_image_url)
    except Exception as e:
        logger.error(f"Failed to process successful generation", extra={'generation_request_id': generation_request_id, 'error': str(e)}, exc_info=True)

        generation_request.status = GenerationRequest.GenerationStatus.FAILED
        generation_request.error_message = "Failed to process successful generation"
        await generation_request.asave(update_fields=['status', 'error_message', 'updated_at'])
        return



def prepare_image_for_upload(image_data, quality):
    if isinstance(image_data, bytes):
        image_file = BytesIO(image_data)
    else:
        image_file = image_data
        image_file.seek(0)

    image = Image.open(image_file)
    transposed_image = ImageOps.exif_transpose(image)

    if transposed_image.mode != "RGB":
        transposed_image = transposed_image.convert("RGB")

    buffer = BytesIO()
    transposed_image.save(buffer, format='JPEG', quality=quality, optimize=True)
    buffer.seek(0)
    
    return buffer.getvalue()

def upload_input_image_to_gcs(image_file, user_id):
    prepared_image_bytes = prepare_image_for_upload(image_file, quality=75)

    timestamp = timezone.now().strftime('%Y-%m-%d-%H-%M-%S')
    bucket_name = settings.GCP_STORAGE_BUCKET_NAME
    blob_name = f"users/{user_id}/images/inputs/input-{timestamp}.jpg"
    
    bucket = gcs_sync_storage_client.bucket(bucket_name)
    blob = bucket.blob(blob_name)
    
    blob.upload_from_string(prepared_image_bytes, content_type='image/jpeg')

    return blob.public_url

def generate_signed_gcs_url(gcs_img_url, expires_in_seconds):
    parsed_url = urlparse(gcs_img_url)
    path = parsed_url.path.lstrip('/')
    bucket_name, blob_name = path.split('/', 1)

    bucket = gcs_sync_storage_client.bucket(bucket_name)
    blob = bucket.blob(blob_name)

    return blob.generate_signed_url(
        expiration=timedelta(seconds=expires_in_seconds),
        version='v4',
        method='GET'
    )

def get_user_gcs_all_blob_names(user_id):
    bucket_name = settings.GCP_STORAGE_BUCKET_NAME
    bucket = gcs_sync_storage_client.bucket(bucket_name)
    prefix = f"users/{user_id}/"
    blobs = bucket.list_blobs(prefix=prefix)
    
    return [blob.name for blob in blobs]