import os
import json
import base64
import logging
import urllib.request
from io import BytesIO
from datetime import timedelta
from PIL import Image, ImageOps
from django.conf import settings
from urllib.parse import urlparse
from openrouter import OpenRouter
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
from openrouter.errors import ResponseValidationError
from gcloud.aio.storage import Storage as GCSAsyncStorage

GCS_KEY_PATH = os.path.join(settings.BASE_DIR, 'core', 'gcs_key.json')
logger = logging.getLogger(__name__)
gcs_sync_storage_client = gcs_sync_storage.Client.from_service_account_json(GCS_KEY_PATH)

class SafetyException(Exception):
    pass

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
        'dispatch_deadline': duration_pb2.Duration(seconds=15)
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

async def generate_output_image(prompt, input_image_bytes, input_image_mime_type):
    base64_input_image = base64.b64encode(input_image_bytes).decode('utf-8')
    
    async with OpenRouter(api_key=settings.OPENROUTER_API_KEY) as client:
        response = await client.chat.send_async(
            model="google/gemini-2.5-flash-image",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text", 
                            "text": prompt
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:{input_image_mime_type};base64,{base64_input_image}"
                            }
                        }
                    ]
                }
            ],
            http_headers={
                "HTTP-Referer": "https://ervelus.com",
                "X-Title": "Ervelus"
            },
            retries=None,
            timeout_ms=40000
        )
        
        choices = getattr(response, 'choices', None) if response else None
        if not isinstance(choices, list) or len(choices) == 0:
            raise SafetyException("OpenRouter returned response with no choices")
            
        message = getattr(choices[0], 'message', None)
        if not message:
            raise SafetyException("OpenRouter response choice contains no message")
            
        images = getattr(message, 'images', None)
        if not isinstance(images, list) or len(images) == 0:
            raise SafetyException("Model returned no images")
            
        image_url = getattr(images[0], 'image_url', None)
        url = getattr(image_url, 'url', None) if image_url else None
        
        if not url:
            raise SafetyException("Model returned image data with no URL")
        
        with urllib.request.urlopen(url) as img_response:
            output_image_bytes = img_response.read()
            
        if not output_image_bytes:
            raise SafetyException("Downloaded image byte data is empty")
            
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
        logger.error("Generation request disappeared. Update after resize aborted", extra={'generation_request_id': generation_request_id})
        return
    except Exception as e:
        logger.error("Failed to update generation request after resize", extra={'generation_request_id': generation_request_id, 'error': str(e)}, exc_info=True)
        return

    try:
        user_profile = await UserProfile.objects.aget(user_id=generation_request.user_id)
        
        if generation_request.type == GenerationRequest.CreditType.FREE:
            if user_profile.free_credits > 0:
                user_profile.free_credits -= 1
                await user_profile.asave(update_fields=['free_credits'])
            else:
                logger.error("No free credits available for debit", extra={'generation_request_id': generation_request_id})
        elif generation_request.type == GenerationRequest.CreditType.PAID:
            if user_profile.paid_credits > 0:
                user_profile.paid_credits -= 1
                await user_profile.asave(update_fields=['paid_credits'])
            else:
                logger.error("No paid credits available for debit", extra={'generation_request_id': generation_request_id})
    except UserProfile.DoesNotExist:
        logger.error("User profile not found for credit debit", extra={'generation_request_id': generation_request_id})
    except Exception as e:
        logger.error("Error during credit debit process", extra={'generation_request_id': generation_request_id, 'error': str(e)}, exc_info=True)

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
        'dispatch_deadline': duration_pb2.Duration(seconds=15)
    }

    tasks_client.create_task(request={'parent': queue_path, 'task': task})

async def handle_generation_process(generation_request_id, input_image_url):
    generation_request_status = None

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
        
        input_file_extension = os.path.splitext(blob_name)[1].lower().lstrip('.')
        mime_type_map = {
            'png': 'image/png',
            'webp': 'image/webp',
            'jpg': 'image/jpeg'
        }
        input_image_mime_type = mime_type_map[input_file_extension]

        await sync_to_async(connections.close_all)()
        output_image_bytes = await generate_output_image(prompt, input_image_bytes, input_image_mime_type)

        output_image_url = await upload_output_image_to_gcs(
            image_bytes=output_image_bytes,
            user_id=user_id,
            style_name=style_name
        )

        generation_request_status = GenerationRequest.GenerationStatus.COMPLETED
    except GenerationRequest.DoesNotExist:
        logger.error("Generation request was deleted. Generation process aborted", extra={'generation_request_id': generation_request_id})
        return
    except SafetyException as e:
        logger.info("Image generation rejected by safety filters", extra={'generation_request_id': generation_request_id, 'error': str(e)}, exc_info=True)
        generation_request_status = GenerationRequest.GenerationStatus.REJECTED_BY_SAFETY
    except ResponseValidationError as e:
        logger.info("Provider rejected input image, returning invalid JSON structure", extra={'generation_request_id': generation_request_id, 'error': str(e)}, exc_info=True)
        generation_request_status = GenerationRequest.GenerationStatus.REJECTED_BY_SAFETY
    except Exception as e:
        logger.error("Error during image generation process", extra={'generation_request_id': generation_request_id, 'error': str(e)}, exc_info=True)
        generation_request_status = GenerationRequest.GenerationStatus.FAILED
    
    try:
        if generation_request_status in [GenerationRequest.GenerationStatus.REJECTED_BY_SAFETY, GenerationRequest.GenerationStatus.FAILED]:
            try:
                await sync_to_async(schedule_image_deletion)([input_image_url])
            except Exception as e:
                logger.error("Failed to schedule image deletion", extra={'generation_request_id': generation_request_id, 'input_image_url': input_image_url, 'error': str(e)}, exc_info=True)

            generation_request.status = generation_request_status
            await generation_request.asave(update_fields=['status', 'updated_at'])
            return
    except Exception as e:
        logger.error("Failed to update generation request status", extra={'generation_request_id': generation_request_id, 'error': str(e)}, exc_info=True)
        return

    try:
        await schedule_image_resizing(
            generation_request_id=generation_request_id,
            user_id=user_id,
            input_image_url=input_image_url,
            output_image_url=output_image_url
        )
    except Exception as e:
        logger.error("Failed to create resizing task", extra={'generation_request_id': generation_request_id, 'error': str(e)}, exc_info=True)