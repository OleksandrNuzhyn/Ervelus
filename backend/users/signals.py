from django.dispatch import receiver
from allauth.socialaccount.signals import pre_social_login
from allauth.account.signals import email_confirmed
from allauth.account.models import EmailAddress
from django.contrib.auth import login
from django.conf import settings
from django.db.models.signals import pre_delete
from django.contrib.auth import get_user_model
import requests
import logging

logger = logging.getLogger(__name__)
User = get_user_model()

@receiver(pre_social_login)
def handle_social_login_verification(sender, request, sociallogin, **kwargs):
    if sociallogin.is_existing:
        user = sociallogin.user
        
        try:
            email_obj = EmailAddress.objects.get(user=user, primary=True)
            
            if not email_obj.verified:
                email_obj.verified = True
                email_obj.save()

        except EmailAddress.DoesNotExist:
            EmailAddress.objects.create(
                user=user,
                email=user.email,
                verified=True,
                primary=True,
            )

@receiver(email_confirmed)
def auto_login_on_email_confirmation(request, email_address, **kwargs):
    user = email_address.user
    login(request, user, backend='allauth.account.auth_backends.AuthenticationBackend')

@receiver(pre_delete, sender=User)
def user_pre_delete_receiver(sender, instance, **kwargs):
    try:
        url = f"{settings.MAILGUN_API_BASE_URL.rstrip('/')}/v3/lists/{settings.MAILGUN_MAILING_LIST_ADDRESS.rstrip('/')}/members/{instance.email}"
        auth = ('api', settings.MAILGUN_API_KEY)
        
        response = requests.delete(url, auth=auth)
        response.raise_for_status()

        logger.info("Successfully removed user from Mailgun list", extra={'user_id': instance.id})
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 404:
            logger.info("User was not found in Mailgun list, no action needed", extra={'user_id': instance.id})
        else:
            logger.error("Failed to remove user from Mailgun list due to HTTP error", extra={'user_id': instance.id, 'status_code': e.response.status_code, 'error': str(e)})
    except requests.exceptions.RequestException as e:
        logger.error("Failed to remove user from Mailgun list", extra={'user_id': instance.id, 'error': str(e)})