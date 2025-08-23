import requests
from django.conf import settings
from generations.services import gcs_sync_storage_client
from django.contrib.auth import get_user_model
import json
import logging

logger = logging.getLogger(__name__)
User = get_user_model()

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

def sync_users_with_mailgun_list():
    try:
        user_emails = list(
            User.objects.filter(
                is_active=True,
                is_staff=False,
                emailaddress__verified=True
            ).values_list('email', flat=True)
        )

        total_users = len(user_emails)
        batch_size = 1000
        is_success = True

        if not user_emails:
            logger.info("No users found to sync with Mailgun")
            return {"is_success": True, "message": "No users found to sync with Mailgun"}

        url = f"{settings.MAILGUN_API_BASE_URL.rstrip('/')}/v3/lists/{settings.MAILGUN_MAILING_LIST_ADDRESS.rstrip('/')}/members.json"
        auth = ('api', settings.MAILGUN_API_KEY)

        for i in range(0, total_users, batch_size):
            if is_success:
                batch = user_emails[i:i+batch_size]
                
                data = {
                    'members': json.dumps(batch),
                    'upsert': 'true'
                }

                try:
                    response = requests.post(url, auth=auth, data=data)
                    response.raise_for_status()
                except requests.exceptions.RequestException as e:
                    is_success = False
                    logger.error(f"Failed to sync batch with Mailgun", extra={'error': e}, exc_info=True)
                    return {"is_success": is_success, "message": "Failed to sync users with Mailgun"}

        logger.info(f"Mailgun sync completed successfully for {total_users} users")
        return {"is_success": is_success, "message": f"Mailgun sync completed successfully for {total_users} users"}
    except Exception as e:
        logger.error(f"An unexpected error occurred during Mailgun sync", extra={'error': e}, exc_info=True)
        return {"is_success": False, "message": "An unexpected error occurred during Mailgun sync"}