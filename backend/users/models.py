from datetime import datetime, timezone
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from rest_framework.authtoken.models import Token
from django.conf import settings
from django.db import models
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
        instance.date_joined = datetime.fromtimestamp(0, tz=timezone.utc)

    def export(self, instance):
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


class UserProfile(models.Model):
    class Meta:
        verbose_name = 'User Profile'
        verbose_name_plural = 'User Profiles'

    class PrivacyMeta:
        fields = [
            'telegram_id',
        ]
        search_fields = [
            'user__email',
        ]
        export_fields = [
            'telegram_id',
            'credits'
        ]

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='profile')
    telegram_id = models.CharField(max_length=255, unique=True, null=True, blank=True)
    credits = models.IntegerField(default=2)

    def __str__(self):
        return f'Profile {self.user.email}'


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