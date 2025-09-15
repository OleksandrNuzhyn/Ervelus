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
from django.utils import timezone
from django.db.models import Q
import json

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
    file_name = f"user_data_retention/{user.email}_{timezone.now().strftime('%Y%m%d%H%M%S')}.json"
    bucket_name = settings.GCP_STORAGE_BUCKET_NAME
    bucket = gcs_sync_storage_client.bucket(bucket_name)
    blob = bucket.blob(file_name)

    json_data = json.dumps(user_data_for_retention, cls=DjangoJSONEncoder, indent=4)
    blob.upload_from_string(json_data, content_type='application/json')
    LogEntry.objects.log_create(
        instance=user,
        action=LogEntry.Action.ACCESS,
        changes='User data retained to GCS for account deletion',
        additional_data={"gdpr_deletion_process": True}
    )

def delete_user_images_from_gcs(user):
    try:
        bucket_name = settings.GCP_STORAGE_BUCKET_NAME
        bucket = gcs_sync_storage_client.bucket(bucket_name)

        prefix = f"users/{user.id}/"
        blobs_to_delete = list(bucket.list_blobs(prefix=prefix))

        if not blobs_to_delete:
            LogEntry.objects.log_create(
                instance=user,
                action=LogEntry.Action.ACCESS,
                changes='No user images to delete from GCS',
                additional_data={"gdpr_deletion_process": True}
            )
            return
        
        for i in range(0, len(blobs_to_delete), 100):
            with gcs_sync_storage_client.batch():
                for blob in blobs_to_delete[i:i+100]:
                    blob.delete()
        
        LogEntry.objects.log_create(
            instance=user,
            action=LogEntry.Action.ACCESS,
            changes=f'Successfully deleted {len(blobs_to_delete)} user images from GCS',
            additional_data={"gdpr_deletion_process": True}
        )
    except Exception as e:
        LogEntry.objects.log_create(
            instance=user,
            action=LogEntry.Action.ACCESS,
            changes=f'Failed to delete user images from GCS: {str(e)}',
            additional_data={"gdpr_deletion_process": True}
        )

def archive_paddle_customer(user):
    if not hasattr(user, 'profile') or not user.profile.paddle_customer_id:
        LogEntry.objects.log_create(
            instance=user,
            action=LogEntry.Action.ACCESS,
            changes='Skipped archiving user in Paddle: no customer ID found',
            additional_data={"gdpr_deletion_process": True}
        )
        return

    customer_id = user.profile.paddle_customer_id
    url = f"{settings.PADDLE_API_BASE_URL.rstrip('/')}/customers/{customer_id}"
    headers = {
        "Authorization": f"Bearer {settings.PADDLE_API_KEY}",
        "Content-Type": "application/json",
    }
    data = {"status": "archived"}

    try:
        response = requests.patch(url, headers=headers, json=data)
        response.raise_for_status()
        LogEntry.objects.log_create(
            instance=user,
            action=LogEntry.Action.ACCESS,
            changes='Successfully archived user in Paddle',
            additional_data={"gdpr_deletion_process": True}
        )
    except requests.exceptions.HTTPError as e:
        LogEntry.objects.log_create(
            instance=user,
            action=LogEntry.Action.ACCESS,
            changes=f'Failed to archive user in Paddle: HTTP {e.response.status_code}',
            additional_data={"gdpr_deletion_process": True}
        )
    except requests.exceptions.RequestException as e:
        LogEntry.objects.log_create(
            instance=user,
            action=LogEntry.Action.ACCESS,
            changes=f'Failed to archive user in Paddle: {str(e)}',
            additional_data={"gdpr_deletion_process": True}
        )

def remove_user_from_mailgun_list(user):
    try:
        url = f"{settings.MAILGUN_API_BASE_URL.rstrip('/')}/v3/lists/{settings.MAILGUN_MAILING_LIST_ADDRESS.rstrip('/')}/members/{user.email}"
        auth = ('api', settings.MAILGUN_API_KEY)
        
        response = requests.delete(url, auth=auth)
        response.raise_for_status()

        LogEntry.objects.log_create(
            instance=user,
            action=LogEntry.Action.ACCESS,
            changes='Successfully removed user from Mailgun list',
            additional_data={"gdpr_deletion_process": True}
        )
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 404:
            LogEntry.objects.log_create(
                instance=user,
                action=LogEntry.Action.ACCESS,
                changes='User was not found in Mailgun list',
                additional_data={"gdpr_deletion_process": True}
            )
        else:
            LogEntry.objects.log_create(
                instance=user,
                action=LogEntry.Action.ACCESS,
                changes=f'Failed to remove user from Mailgun list: HTTP {e.response.status_code}',
                additional_data={"gdpr_deletion_process": True}
            )
    except requests.exceptions.RequestException as e:
        LogEntry.objects.log_create(
            instance=user,
            action=LogEntry.Action.ACCESS,
            changes=f'Failed to remove user from Mailgun list: {str(e)}',
            additional_data={"gdpr_deletion_process": True}
        )

def delete_user_audit_records(user):
    log_entries_to_delete = Q(actor=user)

    objects_to_check = [
        user,
        *user.subscriptions.all(),
        *user.agreements.all(),
        *user.generation_requests.all(),
        *user.emailaddress_set.all(),
        *user.socialaccount_set.all()
    ]

    if hasattr(user, 'profile'):
        objects_to_check.append(user.profile)

    for obj in objects_to_check:
        if obj is None:
            continue
        ct = ContentType.objects.get_for_model(obj)
        log_entries_to_delete |= Q(content_type=ct, object_pk=str(obj.pk))

    LogEntry.objects.filter(log_entries_to_delete) \
        .exclude(additional_data__gdpr_deletion_process=True) \
        .exclude(additional_data__gdpr_export_process=True) \
        .delete()

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
                    return {"is_success": is_success, "message": "Failed to sync users with Mailgun"}

        return {"is_success": is_success, "message": f"Mailgun sync completed successfully for {total_users} users"}
    except Exception as e:
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
        return []
    
    return templates

def send_email(recipient, template_name):
    try:
        url = f"{settings.MAILGUN_API_BASE_URL.rstrip('/')}/{settings.MAILGUN_SENDER_DOMAIN.rstrip('/')}/messages"
        auth = ("api", settings.MAILGUN_API_KEY)
        
        data = {
            "from": f"Ervelus Support <{settings.DEFAULT_FROM_EMAIL}>",
            "to": recipient,
            "template": template_name
        }

        response = requests.post(url, auth=auth, data=data)
        response.raise_for_status()

        return {"is_success": True, "message": f'Email with template "{template_name}" sent to {recipient}'}
    except Exception as e:
        return {"is_success": False, "message": "Failed to send email"}