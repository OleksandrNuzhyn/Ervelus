import os
import json
import logging
from io import BytesIO
from google import genai
from datetime import timedelta
from google.genai import types
from google.genai import errors
from PIL import Image, ImageOps
from django.conf import settings
from urllib.parse import urlparse
from django.utils import timezone
from django.db import connections
from users.models import UserProfile
from django.utils.text import slugify
from .models import GenerationRequest
from asgiref.sync import sync_to_async
from google.protobuf import duration_pb2
from generations.views import tasks_client
from google.cloud.tasks_v2.types import HttpMethod
from google.cloud import storage as gcs_sync_storage
from gcloud.aio.storage import Storage as GCSAsyncStorage
from google.genai.types import HarmCategory, HarmBlockThreshold
from tenacity import retry, wait_random_exponential, retry_if_exception, stop_after_delay

GCS_KEY_PATH = os.path.join(settings.BASE_DIR, 'core', 'gcs_key.json')
logger = logging.getLogger(__name__)
genai_client = None
gcs_sync_storage_client = gcs_sync_storage.Client.from_service_account_json(GCS_KEY_PATH)

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

def schedule_image_deletion(image_urls):
    target_url = f"{settings.BACKGROUND_WORKER_URL.rstrip('/')}/image-delete"
    
    event_data = {
        "image_urls": image_urls
    }

    queue_path = tasks_client.queue_path(
        settings.GCP_PROJECT_ID,
        settings.GCP_TASKS_LOCATION,
        settings.GCP_TASKS_DELETE_EVENTS_QUEUE_ID,
    )

    task = {
        'http_request': {
            'url': target_url,
            'http_method': HttpMethod.POST,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps(event_data).encode('utf-8'),
        },
        'dispatch_deadline': duration_pb2.Duration(seconds=60)
    }

    tasks_client.create_task(request={'parent': queue_path, 'task': task})

def upload_input_image_to_gcs(image_file, user_id):
    extension_for_pillow = os.path.splitext(image_file.name)[1].lower()
    save_format = Image.EXTENSION[extension_for_pillow]

    image_file.seek(0)

    image = Image.open(image_file)
    image = ImageOps.exif_transpose(image)

    buffer = BytesIO()
    image.save(buffer, format=save_format)

    content_type = Image.MIME.get(save_format)
    file_extension = extension_for_pillow.lstrip('.').replace('jpeg', 'jpg')

    timestamp = timezone.now().strftime('%Y-%m-%d-%H-%M-%S')
    bucket_name = settings.GCP_TEMP_BUCKET_NAME
    blob_name = f"users/{user_id}/inputs/input-{timestamp}.{file_extension}"
    
    bucket = gcs_sync_storage_client.bucket(bucket_name)
    blob = bucket.blob(blob_name)
    
    blob.upload_from_string(buffer.getvalue(), content_type=content_type)

    return f"https://storage.googleapis.com/{bucket_name}/{blob_name}"

async def upload_output_image_to_gcs(image_bytes, user_id, style_name):
    slugified_style_name = slugify(style_name)
    timestamp = timezone.now().strftime('%Y-%m-%d-%H-%M-%S')

    content_type = 'image/png'
    file_extension = 'png'

    bucket_name = settings.GCP_TEMP_BUCKET_NAME
    blob_name = f"users/{user_id}/outputs/{slugified_style_name}-{timestamp}.{file_extension}"

    async with GCSAsyncStorage() as gcs_async_storage_client:
        await gcs_async_storage_client.upload(bucket_name, blob_name, image_bytes, content_type=content_type)

    return f"https://storage.googleapis.com/{bucket_name}/{blob_name}"



class ContentBlockedError(Exception):
    pass

def is_retryable_error(error):
    if isinstance(error, errors.ServerError):
        return True
        
    if isinstance(error, errors.ClientError) and hasattr(error, 'code') and error.code == 429:
        return True
    return False



def get_genai_client():
    global genai_client
    
    if genai_client is None:
        genai_client = genai.Client(vertexai=True, project=settings.GCP_PROJECT_ID, location='global')

    return genai_client

@retry(wait=wait_random_exponential(multiplier=2, min=5, max=60), stop=stop_after_delay(45), retry=retry_if_exception(is_retryable_error))
async def generate_output_image_client(genai_client, model, contents, config):
    return await genai_client.aio.models.generate_content(
        model=model,
        contents=contents,
        config=config
    )

async def generate_output_image(prompt, input_image_bytes):
    image = Image.open(BytesIO(input_image_bytes))
    genai_client = get_genai_client()

    response = await generate_output_image_client(
        genai_client=genai_client,
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

    if not response.candidates or not response.candidates[0].content:
        raise ContentBlockedError()

    output_image_bytes = None
    
    for part in response.candidates[0].content.parts:
        if part.inline_data:
            output_image_bytes = part.inline_data.data
            break

    return output_image_bytes

async def handle_update_after_resize(generation_request_id, update_data):
    try:
        generation_request = await GenerationRequest.objects.aget(id=generation_request_id)

        update_fields = []
        for key, value in update_data.items():
            setattr(generation_request, key, value)
            update_fields.append(key)
        
        if update_fields:
            update_fields.append('updated_at')
            await generation_request.asave(update_fields=update_fields)
    except GenerationRequest.DoesNotExist:
        logger.error("Generation request was deleted. Update after resize aborted", extra={'generation_request_id': generation_request_id, 'update_data': update_data})
    except Exception as e:
        logger.error("An error occurred while updating generation request after resize", extra={'generation_request_id': generation_request_id, 'update_data': update_data, 'error': str(e)}, exc_info=True)

@sync_to_async
def schedule_image_resizing(generation_request_id, user_id, input_image_url, output_image_url):
    target_url = f"{settings.BACKGROUND_WORKER_URL.rstrip('/')}/image-resize"
    
    event_data = {
        "generation_request_id": generation_request_id,
        "user_id": user_id,
        "input_image_url": input_image_url,
        "output_image_url": output_image_url
    }

    queue_path = tasks_client.queue_path(
        settings.GCP_PROJECT_ID,
        settings.GCP_TASKS_LOCATION,
        settings.GCP_TASKS_RESIZE_EVENTS_QUEUE_ID,
    )

    task = {
        'http_request': {
            'url': target_url,
            'http_method': HttpMethod.POST,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps(event_data).encode('utf-8'),
        },
        'dispatch_deadline': duration_pb2.Duration(seconds=60)
    }

    tasks_client.create_task(request={'parent': queue_path, 'task': task})

async def handle_generation_process(generation_request_id, input_image_url):
    output_image_url = None
    generation_request_status = None
    error_message = None

    try:
        generation_request = await GenerationRequest.objects.select_related('user', 'chosen_style').aget(id=generation_request_id)

        if not all([
            generation_request.chosen_style,
            generation_request.chosen_style.prompt_template,
            generation_request.chosen_style.name,
            generation_request.user
        ]):
            raise Exception("Missing input data")
        
        prompt = generation_request.chosen_style.prompt_template
        style_name = generation_request.chosen_style.name
        user_id = generation_request.user.id

        parsed_url = urlparse(input_image_url)
        path = parsed_url.path.lstrip('/')
        bucket_name, blob_name = path.split('/', 1)

        async with GCSAsyncStorage() as gcs_async_storage_client:
            input_image_bytes = await gcs_async_storage_client.download(bucket_name, blob_name)
    
        await sync_to_async(connections.close_all)()
        output_image_bytes = await generate_output_image(prompt, input_image_bytes)

        if not output_image_bytes:
            raise Exception("Generated image data is empty")
        
        output_image_url = await upload_output_image_to_gcs(
            image_bytes=output_image_bytes,
            user_id=user_id,
            style_name=style_name
        )

        user_profile = await UserProfile.objects.aget(user_id=user_id)

        if user_profile.credits > 0:
            user_profile.credits -= 1
            await user_profile.asave(update_fields=['credits'])
        else:
            logger.error("Credit not debited, no credits available", extra={'generation_request_id': generation_request_id})

        generation_request_status = GenerationRequest.GenerationStatus.COMPLETED
    except GenerationRequest.DoesNotExist:
        logger.error("Generation request was deleted. Generation process aborted", extra={'generation_request_id': generation_request_id})
        return
    except ContentBlockedError:
        generation_request_status = GenerationRequest.GenerationStatus.REJECTED_BY_SAFETY
        error_message = "Rejected by the safety system"
    except Exception as e:
        logger.error("Error during image generation process", extra={'generation_request_id': generation_request_id, 'error': str(e)}, exc_info=True)
        generation_request_status = GenerationRequest.GenerationStatus.FAILED
        error_message = str(e)
    
    try:
        if generation_request_status:
            update_fields = {
                'status': generation_request_status,
                'error_message': error_message,
                'updated_at': timezone.now()
            }

            if generation_request_status == GenerationRequest.GenerationStatus.REJECTED_BY_SAFETY:
                update_fields['is_visible'] = True
                try:
                    await sync_to_async(schedule_image_deletion)([input_image_url])
                except Exception as e:
                    logger.error("Failed to schedule image deletion", extra={'generation_request_id': generation_request_id, 'input_image_url': input_image_url, 'error': str(e)}, exc_info=True)

            rows_affected = await GenerationRequest.objects.filter(id=generation_request_id).aupdate(**update_fields)

            if rows_affected == 0:
                logger.error("Generation request was deleted before status update", extra={'generation_request_id': generation_request_id})
                
                try:
                    await sync_to_async(schedule_image_deletion)([input_image_url, output_image_url])
                except Exception as e:
                    logger.error("Failed to schedule image deletion", extra={'generation_request_id': generation_request_id, 'output_image_url': output_image_url, 'error': str(e)}, exc_info=True)
                return
    except Exception as e:
        logger.error("Failed to update generation request status", extra={'generation_request_id': generation_request_id, 'error': str(e)}, exc_info=True)
        return

    if generation_request_status in [GenerationRequest.GenerationStatus.COMPLETED, GenerationRequest.GenerationStatus.FAILED]:
        try:
            await schedule_image_resizing(
                generation_request_id=generation_request_id,
                user_id=user_id,
                input_image_url=input_image_url,
                output_image_url=output_image_url
            )
        except Exception as e:
            logger.error("Failed to create resizing task", extra={'generation_request_id': generation_request_id, 'error': str(e)}, exc_info=True)