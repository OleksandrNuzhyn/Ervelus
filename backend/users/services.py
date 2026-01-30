from django.core.serializers.json import DjangoJSONEncoder
from generations.services import gcs_sync_storage_client
from django.contrib.auth import get_user_model
from agreements.models import UserAgreement
from payments.models import UserPurchase
from generations import services
from django.utils import timezone
from django.conf import settings
import logging
import json

User = get_user_model()
logger = logging.getLogger(__name__)

def get_user_data_for_retention(user):
    user_data = {
        "user": {
            "id": user.id,
            "email": user.email,
            "telegram_id": getattr(user.profile, 'telegram_id', None) if hasattr(user, 'profile') else None
        },
        "agreements": [],
        "purchases": [],
        "audit_records": []
    }

    agreements = UserAgreement.objects.filter(user=user)
    user_data["agreements"] = list(agreements.values())

    purchases = UserPurchase.objects.filter(user=user)
    user_data["purchases"] = list(purchases.values())

    return user_data

def upload_user_data_for_retention_to_gcs(user, user_data_for_retention):
    file_name = f"{user.email}-{timezone.now().strftime('%Y-%m-%d-%H-%M')}.json"
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

    services.schedule_image_deletion(image_urls)