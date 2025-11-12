import requests
from django.conf import settings
from generations.services import gcs_sync_storage_client
from django.contrib.auth import get_user_model
from auditlog.models import LogEntry
from .models import UserProfile
from agreements.models import UserAgreement
from subscriptions.models import UserSubscription
from django.core.serializers.json import DjangoJSONEncoder
from django.contrib.contenttypes.models import ContentType
from generations import services
from django.utils import timezone
from django.db.models import Q
import logging
import json

User = get_user_model()
logger = logging.getLogger(__name__)

def get_user_uncancelled_paddle_subscriptions(customer_id):
    url = f"{settings.PADDLE_API_BASE_URL.rstrip('/')}/subscriptions?customer_id={customer_id}&status=active,past_due&scheduled_change_action=pause,resume,none"
    headers = {
        "Authorization": f"Bearer {settings.PADDLE_API_KEY}",
        "Content-Type": "application/json",
    }
    
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    uncancelled_subscriptions = response.json().get('data', [])
    
    return uncancelled_subscriptions

def create_customer_portal_session(customer_id):
    url = f"{settings.PADDLE_API_BASE_URL.rstrip('/')}/customers/{customer_id}/portal-sessions"
    headers = {
        'Authorization': f"Bearer {settings.PADDLE_API_KEY}",
        'Content-Type': 'application/json'
    }

    response = requests.post(url, headers=headers)
    response.raise_for_status()
    response_data = response.json()
    
    return response_data.get('data', {}).get('urls', {}).get('general', {}).get('overview')



def get_user_data_for_retention(user):
    user_data = {
        "user": {
            "id": user.id, 
            "email": user.email
        },
        "profile": None,
        "agreements": [],
        "subscriptions": [],
        "audit_records": []
    }

    try:
        profile = UserProfile.objects.get(user=user)
        user_data["profile"] = {"paddle_customer_id": profile.paddle_customer_id}
    except UserProfile.DoesNotExist:
        pass

    agreements = UserAgreement.objects.filter(user=user)
    user_data["agreements"] = list(agreements.values())

    subscriptions = UserSubscription.objects.filter(user=user)
    user_data["subscriptions"] = list(subscriptions.values())
    
    log_entries_query = Q(actor=user)

    objects_to_check = [
        user,
        *user.subscriptions.all(),
    ]

    if hasattr(user, 'profile'):
        objects_to_check.append(user.profile)

    for obj in objects_to_check:
        if obj is None:
            continue
        ct = ContentType.objects.get_for_model(obj)
        log_entries_query |= Q(content_type=ct, object_pk=str(obj.pk))

    audit_records = LogEntry.objects.filter(log_entries_query).distinct()

    user_data["audit_records"] = [
        {
            'object_pk': record.object_pk,
            'object_repr': record.object_repr,
            'action': record.get_action_display(),
            'changes': record.changes_str,
            'timestamp': record.timestamp,
            'actor_id': record.actor_id,
            'content_type_id': record.content_type_id,
            'remote_addr': record.remote_addr
        }
        for record in audit_records
    ]

    return user_data

def upload_user_data_for_retention_to_gcs(user, user_data_for_retention):
    file_name = f"user_data/{user.email}_{timezone.now().strftime('%Y%m%d%H%M%S')}.json"
    bucket_name = settings.GCP_STORAGE_BUCKET_NAME
    bucket = gcs_sync_storage_client.bucket(bucket_name)
    blob = bucket.blob(file_name)

    json_data = json.dumps(user_data_for_retention, cls=DjangoJSONEncoder, indent=4)
    blob.upload_from_string(json_data, content_type='application/json')



def remove_user_from_mailgun_list(user):
    url = f"{settings.MAILGUN_API_BASE_URL.rstrip('/')}/lists/{settings.MAILGUN_MAILING_LIST_ADDRESS.rstrip('/')}/members/{user.email}"
    auth = ('api', settings.MAILGUN_API_KEY)
    
    response = requests.delete(url, auth=auth)
    response.raise_for_status()

def archive_paddle_customer(user):
    customer_id = user.profile.paddle_customer_id
    url = f"{settings.PADDLE_API_BASE_URL.rstrip('/')}/customers/{customer_id}"
    headers = {
        "Authorization": f"Bearer {settings.PADDLE_API_KEY}",
        "Content-Type": "application/json",
    }
    data = {"status": "archived"}

    response = requests.patch(url, headers=headers, json=data)
    response.raise_for_status()

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

def delete_user_audit_records(user, related_objects_ids):
    related_logs_query = Q(actor=user)

    for ct, pk in related_objects_ids:
        related_logs_query |= Q(content_type=ct, object_pk=pk)

    all_related_logs = LogEntry.objects.filter(related_logs_query)

    gdpr_logs_query = Q(additional_data__gdpr_deletion_process=True) | Q(additional_data__gdpr_export_process=True)

    logs_to_anonymise = all_related_logs.filter(gdpr_logs_query)
    logs_to_anonymise.update(
        actor_email='',
        object_repr=f"Anonymised record of user_id: {user.pk}",
        actor=None,
        remote_addr=None
    )

    logs_to_delete = all_related_logs.exclude(gdpr_logs_query)
    logs_to_delete.delete()



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
            return {"is_success": True, "message": "No users found to sync with Mailgun"}

        url = f"{settings.MAILGUN_API_BASE_URL.rstrip('/')}/lists/{settings.MAILGUN_MAILING_LIST_ADDRESS.rstrip('/')}/members.json"
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
                    logger.error("Failed to sync users with Mailgun", extra={'error': str(e)}, exc_info=True)
                    return {"is_success": is_success, "message": "Failed to sync users with Mailgun"}
        return {"is_success": is_success, "message": f"Mailgun sync completed successfully for {total_users} users"}
    except Exception as e:
        logger.error("Failed to sync users with Mailgun", extra={'error': str(e)}, exc_info=True)
        return {"is_success": False, "message": "An unexpected error occurred during Mailgun sync"}

def get_mailgun_template_list():
    url = f"{settings.MAILGUN_API_BASE_URL.rstrip('/')}/{settings.MAILGUN_SENDER_DOMAIN.rstrip('/')}/templates"
    auth = ("api", settings.MAILGUN_API_KEY)
    templates = []
    
    try:
        response = requests.get(url, auth=auth)
        response.raise_for_status()
        data = response.json()
        
        for item in data.get('items', []):
            templates.append((item['name'], item['name']))
    except Exception as e:
        logger.error("Failed to get Mailgun template list", extra={'error': str(e)}, exc_info=True)
        return []
    
    return templates

def send_email(recipient, template_name):
    url = f"{settings.MAILGUN_API_BASE_URL.rstrip('/')}/{settings.MAILGUN_SENDER_DOMAIN.rstrip('/')}/messages"
    auth = ("api", settings.MAILGUN_API_KEY)
    
    data = {
        "from": settings.DEFAULT_FROM_EMAIL,
        "to": recipient,
        "template": template_name
    }
    
    try:
        response = requests.post(url, auth=auth, data=data)
        response.raise_for_status()

        return {"is_success": True, "message": f'Email with template "{template_name}" sent to {recipient}'}
    except Exception as e:
        logger.error("Failed to send email", extra={'error': str(e)}, exc_info=True)
        return {"is_success": False, "message": "Failed to send email"}

def send_support_email(sender_email, text_body):
    url = f"{settings.MAILGUN_API_BASE_URL.rstrip('/')}/{settings.MAILGUN_SENDER_DOMAIN.rstrip('/')}/messages"
    auth = ("api", settings.MAILGUN_API_KEY)
    
    data = {
        "from": f"Request from {settings.DEFAULT_FROM_EMAIL}",
        "to": "<support@ervelus.com>",
        "subject": f"New letter from {sender_email}",
        "text": text_body
    }
    
    response = requests.post(url, auth=auth, data=data)
    response.raise_for_status()