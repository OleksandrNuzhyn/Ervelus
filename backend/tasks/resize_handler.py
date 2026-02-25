import os
import io
import json
import logging
import logging.config
from PIL import Image
from google.cloud import storage
from urllib.parse import urlparse
from google.cloud import tasks_v2
from google.protobuf import duration_pb2
from google.cloud.tasks_v2.types import HttpMethod

GCP_STORAGE_BUCKET_NAME = os.getenv("GCP_STORAGE_BUCKET_NAME")
GCP_PROJECT_ID = os.getenv("GCP_PROJECT_ID")
GCP_TASKS_LOCATION = os.getenv("GCP_TASKS_LOCATION")
GCP_TASKS_GENERATION_EVENTS_QUEUE_ID = os.getenv("GCP_TASKS_GENERATION_EVENTS_QUEUE_ID")
GENERATIONS_WORKER_URL = os.getenv("GENERATIONS_WORKER_URL")

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "google_json_formatter": {
            "()": "pythonjsonlogger.jsonlogger.JsonFormatter",
            "format": "%(message)s",
        }
    },
    "handlers": {
        "google_cloud_handler": {
            "class": "google.cloud.logging.handlers.StructuredLogHandler",
            "formatter": "google_json_formatter"
        },
    },
    "root": {
        "handlers": ["google_cloud_handler"],
        "level": "INFO",
    }
}

logging.config.dictConfig(LOGGING)
storage_client = storage.Client()
tasks_client = tasks_v2.CloudTasksClient()

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
        final_urls['input_thumb_url'] = f"https://storage.googleapis.com/{GCP_STORAGE_BUCKET_NAME}/{thumb_path}"
        final_urls['input_large_url'] = f"https://storage.googleapis.com/{GCP_STORAGE_BUCKET_NAME}/{large_path}"
    elif folder_type == 'outputs':
        original_path = f"users/{user_id}/outputs/original/{base_name}.jpeg"
        thumb_path = f"users/{user_id}/outputs/thumb/{base_name}.webp"
        large_path = f"users/{user_id}/outputs/large/{base_name}.webp"
        resized_images.append(prepare_resized_image(image, None, 'JPEG', 100, original_path))
        resized_images.append(prepare_resized_image(image, (200, 200), 'WEBP', 80, thumb_path))
        resized_images.append(prepare_resized_image(image, (1000, 1000), 'WEBP', 85, large_path, allow_upscale=True))
        final_urls['output_original_url'] = f"https://storage.googleapis.com/{GCP_STORAGE_BUCKET_NAME}/{original_path}"
        final_urls['output_thumb_url'] = f"https://storage.googleapis.com/{GCP_STORAGE_BUCKET_NAME}/{thumb_path}"
        final_urls['output_large_url'] = f"https://storage.googleapis.com/{GCP_STORAGE_BUCKET_NAME}/{large_path}"

    storage_bucket = storage_client.bucket(GCP_STORAGE_BUCKET_NAME)
    for image_bytes, target_path, content_type in resized_images:
        target_blob = storage_bucket.blob(target_path)
        target_blob.upload_from_string(image_bytes, content_type=content_type)
    
    return final_urls

def create_update_task(generation_request_id, update_data):
    try:
        target_url = f"{GENERATIONS_WORKER_URL.rstrip('/')}/webhooks/generations/tasks/"

        event_data = {
            "task_type": "update_after_resize",
            "payload": {
                "generation_request_id": generation_request_id,
                "update_data": update_data
            }
        }

        queue_path = tasks_client.queue_path(
            GCP_PROJECT_ID,
            GCP_TASKS_LOCATION,
            GCP_TASKS_GENERATION_EVENTS_QUEUE_ID,
        )

        task = {
            'http_request': {
                'url': target_url,
                'http_method': HttpMethod.POST,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps(event_data).encode('utf-8')
            },
            'dispatch_deadline': duration_pb2.Duration(seconds=15)
        }

        tasks_client.create_task(request={'parent': queue_path, 'task': task})
    except Exception as e:
        logging.error("Failed to create task", extra={'generation_request_id': generation_request_id, 'error': str(e)}, exc_info=True)

def image_resize(data):
    user_id = data.get("user_id")
    generation_request_id = data.get("generation_request_id")
    input_image_url = data.get("input_image_url")
    output_image_url = data.get("output_image_url")

    if not generation_request_id or not user_id:
        logging.error("Request is missing required fields", extra={'data': data})
        return

    if not input_image_url and not output_image_url:
        logging.error("No URLs to process", extra={'data': data})
        return

    blobs_to_delete = []
    update_data = {}

    try:
        if input_image_url:
            input_blob = get_blob_from_url(input_image_url)

            if input_blob.exists():
                urls = process_image_resize(input_blob, user_id)
                update_data.update(urls)
                blobs_to_delete.append(input_blob)

        if output_image_url:
            output_blob = get_blob_from_url(output_image_url)

            if output_blob.exists():
                urls = process_image_resize(output_blob, user_id)
                update_data.update(urls)
                blobs_to_delete.append(output_blob)

        if update_data:
            update_data['status'] = 'completed'
            create_update_task(generation_request_id, update_data)
            
        if blobs_to_delete:
            for blob in blobs_to_delete:
                try:
                    blob.delete()
                except Exception as e:
                    logging.error("Failed to delete temporary blob", extra={'generation_request_id': generation_request_id, 'blob_name': blob.name, 'error': str(e)}, exc_info=True)
    except Exception as e:
        logging.error("Failed to process image resize", extra={'data': data, 'error': str(e)}, exc_info=True)