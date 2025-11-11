from collections import defaultdict
from urllib.parse import urlparse
from google.cloud import storage
import logging.config

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

def image_delete(data):
    image_urls = data.get("image_urls")

    if not image_urls:
        logging.error("No image urls to delete")
        return

    blobs_by_bucket = defaultdict(list)

    for url in image_urls:
        if not url:
            continue
        
        try:
            path = urlparse(url).path.lstrip('/')
            bucket_name, blob_name = path.split('/', 1)
            blobs_by_bucket[bucket_name].append(blob_name)
        except Exception as e:
            logging.error("Failed to parse GCS URL during deletion", extra={'url': url, 'error': str(e)}, exc_info=True)

    if not blobs_by_bucket:
        logging.error("No blobs to delete")
        return

    for bucket_name, blob_names in blobs_by_bucket.items():
        try:
            bucket = storage_client.bucket(bucket_name)
            
            prefix = f"users/{blob_names[0].split('/')[1]}/"
            existing_blobs = {blob.name for blob in bucket.list_blobs(prefix=prefix)}
            blobs_to_delete = [name for name in blob_names if name in existing_blobs]

            if not blobs_to_delete:
                continue

            batch_size = 100
            for i in range(0, len(blobs_to_delete), batch_size):
                with storage_client.batch():
                    batch = blobs_to_delete[i:i + batch_size]
                    for blob_name in batch:
                        blob = bucket.blob(blob_name)
                        blob.delete()
            
            logging.info(f"Successfully requested deletion", extra={'bucket_name': bucket_name, 'blobs_to_delete': blobs_to_delete})
        except Exception as e:
            logging.error("Failed to process batch deletion for bucket", extra={'bucket_name': bucket_name, 'error': str(e)}, exc_info=True)