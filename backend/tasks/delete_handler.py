from collections import defaultdict
from urllib.parse import urlparse
from google.cloud import storage
import logging

logging.basicConfig(level=logging.INFO)
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
            batch_size = 100

            for i in range(0, len(blob_names), batch_size):
                with storage_client.batch():
                    batch = blob_names[i:i + batch_size]
                    for blob_name in batch:
                        blob = bucket.blob(blob_name)
                        blob.delete()
        except Exception as e:
            logging.error("Failed to process batch deletion for bucket", extra={'bucket_name': bucket_name, 'blob_names': blob_names, 'error': str(e)}, exc_info=True)