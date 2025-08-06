import base64
import uuid
from urllib.parse import urlparse
import io
import httpx
from django.conf import settings
from django.db import transaction
from .models import GenerationRequest
from subscriptions.models import UserSubscription
from tenacity import retry, wait_random_exponential, retry_if_exception
from gcloud.aio.storage import Storage
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

timeout = httpx.Timeout(90.0, connect=5.0)
openai_client = AsyncOpenAI(timeout=timeout, max_retries=0)

@sync_to_async
def b64decode(data):
    return base64.b64decode(data)

@sync_to_async
def read_file_content(file):
    return file.read()

async def upload_image_to_gcs(image_file, user_id, image_source):
    if image_source == 'input':
        content_type = image_file.content_type
        extension = content_type.split('/')[-1]
        if extension == 'jpeg':
            extension = 'jpg'

        image_bytes = await read_file_content(image_file)
    elif image_source == 'output':
        content_type = 'image/jpeg'
        extension = 'jpg'
        image_bytes = image_file

    bucket_name = settings.GCP_STORAGE_BUCKET_NAME
    blob_name = f"users/{user_id}/images/{uuid.uuid4()}.{extension}"

    async with Storage() as gcs_client:
        await gcs_client.upload(bucket_name, blob_name, image_bytes, content_type=content_type)

    return f"https://storage.googleapis.com/{bucket_name}/{blob_name}"

async def handle_generation_process(generation_request_id, resolution):
    try:
        generation_request = await GenerationRequest.objects.select_related('user', 'chosen_style').aget(id=generation_request_id)

        bucket_name = settings.GCP_STORAGE_BUCKET_NAME
        blob_name = urlparse(generation_request.input_img_url).path.lstrip(f'/{bucket_name}/')
        
        async with Storage() as gcs_client:
            input_image_file = await gcs_client.download(bucket_name, blob_name)

        output_image_file = await generate_output_image(
            prompt=generation_request.chosen_style.prompt_template,
            input_image_file=input_image_file,
            resolution=resolution
        )
        
        output_image_url = await upload_image_to_gcs(
            image_file=output_image_file,
            user_id=generation_request.user.id,
            image_source='output'
        )

        await processing_successful_generation(generation_request, output_image_url)
    except BadRequestError as e:
        generation_request.status = GenerationRequest.GenerationStatus.FAILED
        generation_request.error_api_message = str(e)
        await generation_request.asave(update_fields=['status', 'error_api_message'])
    except Exception as e:
        generation_request.status = GenerationRequest.GenerationStatus.FAILED
        generation_request.error_message = str(e)
        await generation_request.asave(update_fields=['status', 'error_message'])

def is_retryable_error(exception):
    return isinstance(exception, (
        APIConnectionError,
        APITimeoutError,
        InternalServerError,
        RateLimitError,
        UnprocessableEntityError
    ))

@retry(wait=wait_random_exponential(min=5, max=60), retry=retry_if_exception(is_retryable_error))
async def generate_output_image(prompt, input_image_file, resolution):
    result = await openai_client.images.edit(
        model="gpt-image-1",
        image=io.BytesIO(input_image_file),
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
    return await b64decode(result.data[0].b64_json)

@sync_to_async
def processing_successful_generation(generation_request, output_image_url):
    with transaction.atomic():
        subscription_for_debiting_credit = generation_request.user.subscriptions.select_for_update().filter(
            status=UserSubscription.SubscriptionStatus.ACTIVE,
            remaining_credits__gt=0
        ).order_by('end_time').first()
        
        if not subscription_for_debiting_credit:
            raise Exception("No active subscription with credits found to debit")

        subscription_for_debiting_credit.remaining_credits -= 1
        subscription_for_debiting_credit.save(update_fields=['remaining_credits'])

        generation_request.output_img_url = output_image_url
        generation_request.status = GenerationRequest.GenerationStatus.COMPLETED
        generation_request.save(update_fields=['output_img_url', 'status'])