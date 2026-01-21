from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from agreements.services import accept_user_document_version
from agreements.models import TermsVersion
from django.core.exceptions import ValidationError
from django.conf import settings
from django.db import transaction
from .models import UserProfile


class CustomAccountAdapter(DefaultAccountAdapter):
    def get_email_confirmation_url(self, request, emailconfirmation):
        return f"{settings.FRONTEND_URL}/verify-email/{emailconfirmation.key}/"


class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    @transaction.atomic
    def save_user(self, request, sociallogin, form=None):
        user = super().save_user(request, sociallogin, form)
        UserProfile.objects.create(user=user)

        required_document_types = [
            TermsVersion.DocumentType.TERMS_OF_SERVICE,
            TermsVersion.DocumentType.PRIVACY_POLICY
        ]

        latest_documents_version_to_accept = TermsVersion.objects.filter(
            document_type__in=required_document_types
        ).order_by('document_type', '-version').distinct('document_type')

        if len(latest_documents_version_to_accept) != len(required_document_types):
            raise ValidationError("We are unable to complete your registration at this time")

        ip_address = request.META.get('HTTP_X_FORWARDED_FOR', '').split(',')[0].strip()
        user_agent = request.META.get('HTTP_USER_AGENT', '')
        context = {"source": "registration_form", "method": "automatic"}

        for latest_document_version_to_accept in latest_documents_version_to_accept:
            accept_user_document_version(
                user=user,
                terms_version=latest_document_version_to_accept,
                ip_address=ip_address,
                user_agent=user_agent,
                context=context
            )
        
        return user