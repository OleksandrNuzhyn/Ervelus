from dj_rest_auth.registration.serializers import RegisterSerializer
from dj_rest_auth.serializers import LoginSerializer
from allauth.account.models import EmailAddress
from allauth.account.utils import send_email_confirmation
from agreements.services import accept_user_document_version
from agreements.models import TermsVersion
from rest_framework import serializers
from django.db import transaction
from .models import UserProfile


class CustomRegisterSerializer(RegisterSerializer):
    username = None

    def validate_email(self, email):
        email_address = EmailAddress.objects.filter(email__iexact=email).first()

        if email_address:
            if email_address.verified:
                raise serializers.ValidationError(("A user is already registered with this email address"))
            else:
                send_email_confirmation(self.context['request'], email_address.user)
                raise serializers.ValidationError(("We have sent a new confirmation email to this address"))
        
        return email.lower()

    @transaction.atomic
    def save(self, request):
        user = super().save(request)
        UserProfile.objects.create(user=user)

        required_document_types = [
            TermsVersion.DocumentType.TERMS_OF_SERVICE,
            TermsVersion.DocumentType.PRIVACY_POLICY
        ]

        latest_documents_version_to_accept = TermsVersion.objects.filter(
            document_type__in=required_document_types
        ).order_by('document_type', '-version').distinct('document_type')

        if len(latest_documents_version_to_accept) != len(required_document_types):
            raise serializers.ValidationError("We are unable to complete your registration at this time")

        ip_address = request.META.get('REMOTE_ADDR')
        user_agent = request.META.get('HTTP_USER_AGENT')
        context = {"source": "registration_form", "method": "checkbox"}

        for latest_document_version_to_accept in latest_documents_version_to_accept:
            accept_user_document_version(
                user=user,
                terms_version=latest_document_version_to_accept,
                ip_address=ip_address,
                user_agent=user_agent,
                context=context
            )
        
        return user


class CustomLoginSerializer(LoginSerializer):
    username = None


class UserCreditsSerializer(serializers.ModelSerializer):
    total_credits = serializers.IntegerField(read_only=True)

    class Meta:
        model = UserProfile
        fields = ['total_credits']

    
class SupportEmailSerializer(serializers.Serializer):
    email = serializers.EmailField()
    text_body = serializers.CharField(max_length=5000)