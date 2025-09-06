from dj_rest_auth.registration.serializers import RegisterSerializer
from dj_rest_auth.serializers import LoginSerializer
from rest_framework import serializers
from allauth.account.models import EmailAddress
from allauth.account.utils import send_email_confirmation
from agreements import services
from django.db import transaction
from .models import UserProfile
import logging

logger = logging.getLogger(__name__)


class CustomRegisterSerializer(RegisterSerializer):
    username = None

    def validate_email(self, email):
        email_address = EmailAddress.objects.filter(email__iexact=email).first()

        if email_address:
            if email_address.verified:
                raise serializers.ValidationError(("A user is already registered with this e-mail address."))
            else:
                send_email_confirmation(self.context['request'], email_address.user)
                raise serializers.ValidationError(("This e-mail address is already associated with an unverified account. We have sent a new confirmation e-mail to this address."))
        
        return email

    @transaction.atomic
    def save(self, request):
        user = super().save(request)
        UserProfile.objects.create(user=user)
        services.user_accept_documents_latest_version(user)
        logger.info(f"User created from classic registration and accepted all agreements", extra={'user_id': user.id})
        
        return user


class CustomLoginSerializer(LoginSerializer):
    username = None


class UserCreditsSerializer(serializers.ModelSerializer):
    total_credits = serializers.IntegerField(read_only=True)

    class Meta:
        model = UserProfile
        fields = ['total_credits']