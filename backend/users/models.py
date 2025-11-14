from datetime import datetime
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from allauth.account.models import EmailAddress
from allauth.socialaccount.models import SocialAccount
from rest_framework.authtoken.models import Token
from django.db import models
from django.db.models import Q, Sum
from django.db.models.functions import Coalesce
from django.conf import settings
from auditlog.models import LogEntry
import gdpr_assist

User = get_user_model()


class UserPrivacyMeta:
    fields = [
        "password",
        "last_login",
        "username",
        "first_name",
        "last_name",
        "email",
        "is_active",
        "date_joined"
    ]
    search_fields = [
        'email',
    ]

    def anonymise_password(self, instance):
        instance.password = make_password(None)

    def anonymise_username(self, instance):
        instance.username = f'user_{instance.pk}'
    
    def anonymise_is_active(self, instance):
        instance.is_active = False

    def anonymise_date_joined(self, instance):
        instance.date_joined = datetime.fromtimestamp(0)

    def export(self, instance):
        LogEntry.objects.log_create(
            instance=instance,
            action=LogEntry.Action.ACCESS,
            changes={},
            additional_data={
                "gdpr_export_process": True,
                "message": "Personal data successfully exported"
            }
        )
        return {
            'last_login': instance.last_login,
            'is_superuser': instance.is_superuser,
            'username': instance.username,
            'first_name': instance.first_name,
            'last_name': instance.last_name,
            'email': instance.email,
            'is_staff': instance.is_staff,
            'is_active': instance.is_active,
            'date_joined': instance.date_joined
        }


gdpr_assist.register(User, UserPrivacyMeta, gdpr_default_manager_name="gdpr_objects")


class UserProfileCreditQuerySet(models.QuerySet):
    def annotate_total_credits(self):
        return self.annotate(
            total_credits=Coalesce(
                Sum(
                    'user__subscriptions__remaining_credits',
                    filter=Q(user__subscriptions__status='active')
                ),
                0
            )
        )


class UserProfileCreditManager(models.Manager):
    def get_queryset(self):
        return UserProfileCreditQuerySet(self.model)

    def annotate_total_credits(self):
        return self.get_queryset().annotate_total_credits()


class UserProfile(models.Model):
    class Meta:
        verbose_name = 'User Profile'
        verbose_name_plural = 'User Profiles'

    class PrivacyMeta:
        can_anonymise = False
        search_fields = [
            'user__email',
        ]
        export_fields = [
            'paddle_customer_id',
        ]

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='profile')
    paddle_customer_id = models.CharField(max_length=50, unique=True, null=True, blank=True)

    objects = UserProfileCreditManager()

    def __str__(self):
        return f'Profile {self.user.email}'


class EmailAddressPrivacyMeta:
    can_anonymise = False
    search_fields = [
        'email',
    ]
    export_fields = [
        'email', 
        'verified', 
        'primary'
    ]


gdpr_assist.register(EmailAddress, EmailAddressPrivacyMeta)


class SocialAccountPrivacyMeta:
    can_anonymise = False
    search_fields = [
        'user__email',
    ]
    export_fields = [
        'provider', 
        'uid', 
        'last_login', 
        'date_joined', 
        'extra_data'
    ]


gdpr_assist.register(SocialAccount, SocialAccountPrivacyMeta)


class TokenPrivacyMeta:
    can_anonymise = False
    search_fields = [
        'user__email',
    ]
    export_fields = [
        'key', 
        'created'
    ]


gdpr_assist.register(Token, TokenPrivacyMeta)