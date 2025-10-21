import os
import io
import django
import logging
from google.cloud import storage
from urllib.parse import urlparse
from django.db import connections
import functions_framework
from PIL import Image

django.setup()

from core.settings import STORAGE_BUCKET_NAME
from generations.models import GenerationRequest
logging.basicConfig(level=logging.INFO)
storage_client = storage.Client()

def get_blob_from_url(gcs_url):
    parsed_url = urlparse(gcs_url)
    path = parsed_url.path.lstrip('/')
    bucket_name, blob_name = path.split('/', 1)

    bucket = storage_client.bucket(bucket_name)
    return bucket.blob(blob_name)

def prepare_resized_image(image, size, file_format, quality, dest_path, allow_upscale=False):
    image_copy = image.copy()

    if size is None:
        pass
    elif allow_upscale:
        ratio = min(size[0] / image_copy.width, size[1] / image_copy.height)
        new_width = int(image_copy.width * ratio)
        new_height = int(image_copy.height * ratio)
        image_copy = image_copy.resize((new_width, new_height), Image.LANCZOS)
    else:
        image_copy.thumbnail(size, Image.LANCZOS)
    
    output = io.BytesIO()
    image_copy.save(output, format=file_format, quality=quality)
    content_type = f"image/{file_format.lower()}"

    return output.getvalue(), dest_path, content_type

def process_image_resize(image_blob, user_id):
    image_bytes = image_blob.download_as_bytes()
    image_file = io.BytesIO(image_bytes)

    image = Image.open(image_file)
    if image.mode != "RGB":
        image = image.convert("RGB")

    parts = image_blob.name.split('/')
    folder_type, filename = parts[2], parts[3]
    base_name, _ = os.path.splitext(filename)

    resized_images = []
    final_urls = {}

    if folder_type == 'inputs':
        thumb_path = f"users/{user_id}/inputs/thumb/{base_name}.webp"
        large_path = f"users/{user_id}/inputs/large/{base_name}.webp"
        resized_images.append(prepare_resized_image(image, (200, 200), 'WEBP', 80, thumb_path))
        resized_images.append(prepare_resized_image(image, (1000, 1000), 'WEBP', 85, large_path, allow_upscale=True))
        final_urls['input_thumb_url'] = f"https://storage.googleapis.com/{STORAGE_BUCKET_NAME}/{thumb_path}"
        final_urls['input_large_url'] = f"https://storage.googleapis.com/{STORAGE_BUCKET_NAME}/{large_path}"
    elif folder_type == 'outputs':
        original_path = f"users/{user_id}/outputs/original/{base_name}.jpeg"
        thumb_path = f"users/{user_id}/outputs/thumb/{base_name}.webp"
        large_path = f"users/{user_id}/outputs/large/{base_name}.webp"
        resized_images.append(prepare_resized_image(image, None, 'JPEG', 100, original_path))
        resized_images.append(prepare_resized_image(image, (200, 200), 'WEBP', 80, thumb_path))
        resized_images.append(prepare_resized_image(image, (1000, 1000), 'WEBP', 85, large_path, allow_upscale=True))
        final_urls['output_original_url'] = f"https://storage.googleapis.com/{STORAGE_BUCKET_NAME}/{original_path}"
        final_urls['output_thumb_url'] = f"https://storage.googleapis.com/{STORAGE_BUCKET_NAME}/{thumb_path}"
        final_urls['output_large_url'] = f"https://storage.googleapis.com/{STORAGE_BUCKET_NAME}/{large_path}"

    storage_bucket = storage_client.bucket(STORAGE_BUCKET_NAME)
    for image_bytes, target_path, content_type in resized_images:
        target_blob = storage_bucket.blob(target_path)
        target_blob.upload_from_string(image_bytes, content_type=content_type)
    
    return final_urls

def execute_image_resize(request):
    request_json = request.get_json(silent=True)
    if not request_json:
        logging.error("Request is missing or has invalid JSON payload")
        return

    generation_request_id = request_json.get("generation_request_id")
    user_id = request_json.get("user_id")
    input_img_url = request_json.get("input_img_url")
    output_img_url = request_json.get("output_img_url")

    if not generation_request_id or not user_id:
        logging.error("Request is missing required fields", extra={'payload': request_json})
        return

    if not input_img_url and not output_img_url:
        logging.error("No URLs to process", extra={'payload': request_json})
        return

    blobs_to_delete = []
    update_data = {}

    try:
        if input_img_url:
            input_blob = get_blob_from_url(input_img_url)

            if input_blob.exists():
                urls = process_image_resize(input_blob, user_id)
                update_data.update(urls)
                blobs_to_delete.append(input_blob)

        if output_img_url:
            output_blob = get_blob_from_url(output_img_url)

            if output_blob.exists():
                urls = process_image_resize(output_blob, user_id)
                update_data.update(urls)
                blobs_to_delete.append(output_blob)

        if update_data:
            update_data['is_visible'] = True
            GenerationRequest.objects.filter(id=generation_request_id).update(**update_data)
    except Exception as e:
        logging.error("Failed to process image resize", extra={'request_json': request_json, 'error': str(e)}, exc_info=True)
    finally:
        if blobs_to_delete:
            for blob in blobs_to_delete:
                try:
                    blob.delete()
                except Exception as e:
                    logging.error("Failed to delete temporary blob", extra={'blob_name': blob.name, 'error': str(e)}, exc_info=True)

@functions_framework.http
def image_resize_handler(request):
    try:
        execute_image_resize(request)
    except Exception as e:
        logging.error(f"An unhandled exception occurred", extra={'error': str(e)}, exc_info=True)
    finally:
        connections.close_all()
    return "OK", 200