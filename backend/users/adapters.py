from allauth.account.adapter import DefaultAccountAdapter
from django.conf import settings
from django.db import transaction
from .models import UserProfile


class CustomAccountAdapter(DefaultAccountAdapter):
    def get_email_confirmation_url(self, request, emailconfirmation):
        return f"{settings.FRONTEND_URL}/confirm-email/{emailconfirmation.key}"

    def save_user(self, request, user, form, commit=True):
        with transaction.atomic():
            user.save()
            UserProfile.objects.create(user=user)
        return user 