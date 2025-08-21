import logging
from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.conf import settings
from django.db import transaction
from .models import UserProfile

logger = logging.getLogger(__name__)


class CustomAccountAdapter(DefaultAccountAdapter):
    def get_email_confirmation_url(self, request, emailconfirmation):
        return f"{settings.FRONTEND_URL}/verify-email/{emailconfirmation.key}/"


class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    @transaction.atomic
    def save_user(self, request, sociallogin, form=None):
        user = super().save_user(request, sociallogin, form)
        user_profile = UserProfile.objects.create(user=user)
        logger.info(f"User created from social registration and accepted all terms. user_id='{user.id}', terms_version='{user_profile.accepted_terms_version}'")
        return user