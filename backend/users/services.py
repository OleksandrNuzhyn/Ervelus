import requests
from django.conf import settings
from generations.services import gcs_sync_storage_client

def get_user_uncancelled_paddle_subscriptions(customer_id):
    url = f"{settings.PADDLE_API_BASE_URL.rstrip('/')}/subscriptions?customer_id={customer_id}&status=active,past_due"
    headers = {
        "Authorization": f"Bearer {settings.PADDLE_API_KEY}",
        "Content-Type": "application/json",
    }
    
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    
    return response.json().get('data', [])

def create_customer_portal_session(customer_id):
    url = f"{settings.PADDLE_API_BASE_URL.rstrip('/')}/customers/{customer_id}/portal-sessions"
    headers = {
        'Authorization': f"Bearer {settings.PADDLE_API_KEY}",
        'Content-Type': 'application/json'
    }

    response = requests.post(url, headers=headers)
    response.raise_for_status()

    response_data = response.json()
    return response_data['data']['urls']['general']['overview']

def delete_user_images_from_gcs(user_id):
    bucket_name = settings.GCP_STORAGE_BUCKET_NAME
    bucket = gcs_sync_storage_client.bucket(bucket_name)

    prefix = f"users/{user_id}/"
    blobs_to_delete = list(bucket.list_blobs(prefix=prefix))

    if not blobs_to_delete:
        return
    
    for i in range(0, len(blobs_to_delete), 100):
        with gcs_sync_storage_client.batch():
            for blob in blobs_to_delete[i:i+100]:
                blob.delete()