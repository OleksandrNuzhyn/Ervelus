from generations.services import gcs_sync_storage_client, schedule_image_deletion
from django.core.serializers.json import DjangoJSONEncoder
from generations.models import GenerationRequest
from django.contrib.auth import get_user_model
from agreements.models import UserAgreement
from core.models import ApplicationConfig
from payments.models import UserPurchase
from django.db import transaction
from django.utils import timezone
from django.conf import settings
from django.db.models import F
import logging
import json

User = get_user_model()
logger = logging.getLogger(__name__)

def get_user_data_for_retention(user):
    return {
        "user": {
            "id": str(user.id)
        },
        "profile": {
            "telegram_id": str(user.profile.telegram_id),
            "credits": str(user.profile.credits)
        },
        "agreements": list(UserAgreement.objects.filter(user=user).values()),
        "purchases": list(UserPurchase.objects.filter(user=user).values())
    }

def upload_user_data_for_retention_to_gcs(user, user_data_for_retention):
    file_name = f"{user.profile.telegram_id or user.id}-{timezone.now().strftime('%Y-%m-%d-%H-%M')}.json"
    bucket_name = settings.GCP_COMPLIANCE_BUCKET_NAME
    bucket = gcs_sync_storage_client.bucket(bucket_name)
    blob = bucket.blob(file_name)

    json_data = json.dumps(user_data_for_retention, cls=DjangoJSONEncoder, indent=4)
    blob.upload_from_string(json_data, content_type='application/json')

def schedule_user_images_deletion(user):
    bucket_name = settings.GCP_STORAGE_BUCKET_NAME
    bucket = gcs_sync_storage_client.bucket(bucket_name)

    prefix = f"users/{user.id}/"
    blobs_to_delete = list(bucket.list_blobs(prefix=prefix))

    if not blobs_to_delete:
        return
    
    image_urls = [
        f"https://storage.googleapis.com/{bucket_name}/{blob.name}"
        for blob in blobs_to_delete
    ]

    schedule_image_deletion(image_urls)

def delete_user_account(user):
    requests_in_process = GenerationRequest.objects.filter(user=user, status=GenerationRequest.GenerationStatus.PROCESSING)

    if requests_in_process.exists():
        logger.error("User deletion with unfinished generations", extra={'user_id': user.id, 'requests_in_process_ids': list(requests_in_process.values_list('id', flat=True))})

    try:
        user_data_for_retention = get_user_data_for_retention(user)
    except Exception as e:
        logger.error("Failed to get user data for retention in delete request", extra={'user_id': user.id, 'error': str(e)}, exc_info=True)
        return False

    try:
        upload_user_data_for_retention_to_gcs(user, user_data_for_retention)
    except Exception as e:
        logger.error("Failed to upload user data for retention to GCS in delete request", extra={'user_id': user.id, 'error': str(e)}, exc_info=True)
        return False

    try:
        schedule_user_images_deletion(user)
    except Exception as e:
        logger.error("Failed to schedule user images deletion in delete request", extra={'user_id': user.id, 'error': str(e)}, exc_info=True)
        return False
    
    try:
        with transaction.atomic():
            if hasattr(user, 'auth_token'):
                user.auth_token.delete()

            for generation_request in user.generation_requests.all():
                generation_request.anonymise()

            for agreement in user.agreements.all():
                agreement.anonymise()

            for promo_code_usage in user.promo_code_usages.all():
                promo_code_usage.anonymise()

            if user.profile.credits > 0:
                config = ApplicationConfig.get_solo()
                config.reserved_generations = F('reserved_generations') - user.profile.credits
                config.save(update_fields=['reserved_generations'])
                
            user.profile.delete()
            user.anonymise()
    except Exception as e:
        logger.error("Failed to anonymise user data in delete request", extra={'user_id': user.id, 'error': str(e)}, exc_info=True)
        return False

    return True