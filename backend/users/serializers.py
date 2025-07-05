from dj_rest_auth.registration.serializers import RegisterSerializer
from dj_rest_auth.serializers import LoginSerializer
from rest_framework import serializers
from allauth.account.models import EmailAddress
from allauth.account.utils import send_email_confirmation

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

class CustomLoginSerializer(LoginSerializer):
    username = None 