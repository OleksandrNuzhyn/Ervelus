import base64
import logging
import uuid
from urllib.parse import urlparse
from datetime import timedelta
import io
import httpx
from django.conf import settings
from django.db import transaction, close_old_connections
from .models import GenerationRequest
from subscriptions.models import UserSubscription
from tenacity import retry, wait_random_exponential, retry_if_exception, stop_after_attempt
from gcloud.aio.storage import Storage as GCSAsyncStorage
from google.cloud import storage as gcs_sync_storage
from asgiref.sync import sync_to_async
from openai import (
    AsyncOpenAI,
    APITimeoutError,
    APIConnectionError,
    BadRequestError,
    RateLimitError,
    InternalServerError,
    UnprocessableEntityError,
)

logger = logging.getLogger(__name__)
timeout = httpx.Timeout(90.0, connect=5.0)
openai_client = AsyncOpenAI(timeout=timeout, max_retries=0)
gcs_sync_storage_client = gcs_sync_storage.Client()

@sync_to_async
def decode_base64(data):
    return base64.b64decode(data)

def upload_input_image_to_gcs(image_file, user_id):
    content_type = image_file.content_type
    extension = content_type.split('/')[-1]
    
    if extension == 'jpeg':
        extension = 'jpg'

    bucket_name = settings.GCP_STORAGE_BUCKET_NAME
    blob_name = f"users/{user_id}/images/inputs/{uuid.uuid4()}.{extension}"
    
    bucket = gcs_sync_storage_client.bucket(bucket_name)
    blob = bucket.blob(blob_name)
    
    blob.upload_from_file(image_file, content_type=content_type)

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
        
        blob = bucket.blob(blob_name)
        blob.delete()

async def upload_output_image_to_gcs(image_bytes, user_id):
    content_type = 'image/jpeg'
    extension = 'jpg'

    bucket_name = settings.GCP_STORAGE_BUCKET_NAME
    blob_name = f"users/{user_id}/images/outputs/{uuid.uuid4()}.{extension}"

    async with GCSAsyncStorage() as gcs_async_storage_client:
        await gcs_async_storage_client.upload(bucket_name, blob_name, image_bytes, content_type=content_type)

    return f"https://storage.googleapis.com/{bucket_name}/{blob_name}"

async def handle_generation_process(generation_request_id, resolution):
    try:
        generation_request = await GenerationRequest.objects.select_related('user', 'chosen_style').aget(id=generation_request_id)
        close_old_connections()

        parsed_url = urlparse(generation_request.input_img_url)
        path = parsed_url.path.lstrip('/')
        bucket_name, blob_name = path.split('/', 1)
        
        async with GCSAsyncStorage() as gcs_async_storage_client:
            metadata = await gcs_async_storage_client.download_metadata(bucket_name, blob_name)
            input_image_content_type = metadata.get('contentType')
            input_image_file = await gcs_async_storage_client.download(bucket_name, blob_name)

        output_image_bytes = await generate_output_image(
            prompt=generation_request.chosen_style.prompt_template,
            input_image_file=input_image_file,
            input_image_content_type=input_image_content_type,
            resolution=resolution
        )
        logger.info(f"Successfully generated image from OpenAI API. generation_request_id='{generation_request_id}'")
        
        output_image_url = await upload_output_image_to_gcs(
            image_bytes=output_image_bytes,
            user_id=generation_request.user.id
        )
        logger.info(f"Successfully uploaded output image to GCS. generation_request_id='{generation_request_id}'")

        await processing_successful_generation(generation_request, output_image_url)
        logger.info(f"Successfully processed generation. generation_request_id='{generation_request_id}'")
    except BadRequestError as e:
        logger.warning(f"BadRequestError during generation. generation_request_id='{generation_request_id}', error='{e}'")
        await sync_to_async(delete_generation_request_images_from_gcs)(generation_request)
        logger.info(f"Successfully deleted GCS images for generation_request_id='{generation_request_id}'")

        generation_request.input_img_url = None
        generation_request.status = GenerationRequest.GenerationStatus.FAILED
        generation_request.error_api_message = "Your request was rejected by the safety system"
        await generation_request.asave(update_fields=['status', 'error_api_message', 'input_img_url', 'updated_at'])
    except Exception as e:
        logger.error(f"Unhandled exception during generation. generation_request_id='{generation_request_id}', error='{e}'", exc_info=True)
        await sync_to_async(delete_generation_request_images_from_gcs)(generation_request)
        logger.info(f"Successfully deleted GCS images for generation_request_id='{generation_request_id}'")

        generation_request.input_img_url = None
        generation_request.status = GenerationRequest.GenerationStatus.FAILED
        generation_request.error_message = "Sorry, something went wrong. Please try again later"
        await generation_request.asave(update_fields=['status', 'error_message', 'input_img_url', 'updated_at'])

def is_retryable_error(exception):
    return isinstance(exception, (
        APIConnectionError,
        APITimeoutError,
        InternalServerError,
        RateLimitError,
        UnprocessableEntityError
    ))

@retry(
    wait=wait_random_exponential(min=1, max=30), 
    stop=stop_after_attempt(6),
    retry=retry_if_exception(is_retryable_error)
)
async def generate_output_image(prompt, input_image_file, input_image_content_type, resolution):
    result = await openai_client.images.edit(
        model="gpt-image-1",
        image=('input_image', io.BytesIO(input_image_file), input_image_content_type),
        prompt=prompt,
        background="opaque",
        input_fidelity="low",
        output_format="jpeg",
        output_compression=100,
        quality="low",
        size=resolution,
        stream=False,
        n=1
    )

    decoded_bytes = await decode_base64(result.data[0].b64_json)

    return decoded_bytes

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
            logger.warning(f"Credit not debited, no active subscription found. generation_request_id='{generation_request.id}'")
            return

        subscription_for_debiting_credit.remaining_credits -= 1
        subscription_for_debiting_credit.save(update_fields=['remaining_credits'])

        generation_request.output_img_url = output_image_url
        generation_request.status = GenerationRequest.GenerationStatus.COMPLETED
        generation_request.save(update_fields=['output_img_url', 'status', 'updated_at'])