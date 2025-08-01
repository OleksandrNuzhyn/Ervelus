import base64
import uuid
from django.conf import settings
from django.db import transaction
from .models import GenerationRequest
from openai import AsyncOpenAI
from gcloud.aio.storage import Storage
from asgiref.sync import sync_to_async
import aiohttp

openai_client = AsyncOpenAI()

async def get_gcs_client():
    return Storage()

@sync_to_async
def read_file_content(file):
    return file.read()

async def upload_image_to_gcs(image_file, user_id, image_source):
    bucket_name = settings.GCP_STORAGE_BUCKET_NAME
    
    if image_source == 'input':
        content_type = image_file.content_type
        extension = content_type.split('/')[-1]
        if extension == 'jpeg':
            extension = 'jpg'
    elif image_source == 'output':
        content_type = 'image/jpeg'
        extension = 'jpg'

    blob_name = f"users/{user_id}/images/{uuid.uuid4()}.{extension}"
    image_bytes = await read_file_content(image_file)

    gcs_client = await get_gcs_client()
    await gcs_client.upload(bucket_name, blob_name, image_bytes, content_type=content_type)

    return f"https://storage.googleapis.com/{bucket_name}/{blob_name}"





async def generate_image_with_openai(prompt: str, input_image_bytes: bytes, resolution: str) -> bytes:
    result = await openai_client.images.edit(
        model="dall-e-2",
        image=input_image_bytes,
        prompt=prompt,
        size=resolution,
        response_format='b64_json'
    )
    return base64.b64decode(result.data[0].b64_json)

async def _debit_credit_and_finalize_request(generation_request, output_url):
    with transaction.atomic():
        subscription_to_debit = await generation_request.user.subscriptions.filter(
            status=generation_request.user.subscriptions.SubscriptionStatus.ACTIVE,
            generations_count__gt=0
        ).order_by('end_time').afirst()
        
        if not subscription_to_debit:
            raise Exception("No active subscription with credits found to debit.")

        subscription_to_debit.generations_count -= 1
        await subscription_to_debit.asave(update_fields=['generations_count'])

        generation_request.output_img_url = output_url
        generation_request.status = GenerationRequest.GenerationStatus.COMPLETED
        await generation_request.asave(update_fields=['output_img_url', 'status'])

async def process_generation_from_event(generation_request_id: int, resolution: str):
    generation_request = None
    
    try:
        generation_request = await GenerationRequest.objects.select_related('user', 'chosen_style').aget(id=generation_request_id)

        # 1. Download input image
        async with aiohttp.ClientSession() as session:
            async with session.get(generation_request.input_img_url) as resp:
                resp.raise_for_status()
                input_image_bytes = await resp.read()

        # 2. Call OpenAI
        generated_image_bytes = await generate_image_with_openai(
            prompt=generation_request.chosen_style.prompt_template,
            input_image_bytes=input_image_bytes,
            resolution=resolution
        )
        
        # 3. Upload result to GCS
        output_url = await upload_image_to_gcs(
            image_file=generated_image_bytes, 
            user_id=generation_request.user.id, 
            image_source='output'
        )

        # 4. Final DB Update (transactional)
        await _debit_credit_and_finalize_request(generation_request, output_url)

    except Exception as e:
        if generation_request:
            generation_request.status = GenerationRequest.GenerationStatus.FAILED
            generation_request.error_message = str(e)
            await generation_request.asave(update_fields=['status', 'error_message']) 