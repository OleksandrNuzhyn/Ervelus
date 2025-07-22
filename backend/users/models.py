from django.db import models
from django.conf import settings
from django.utils import timezone
import uuid

def get_current_terms_version():
    return settings.CURRENT_TERMS_VERSION


class UserProfile(models.Model):
    class Meta:
        verbose_name = 'User Profile'
        verbose_name_plural = 'User Profiles'

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile', editable=False)
    paddle_customer_id = models.CharField(max_length=40, unique=True, null=True, blank=True)
    terms_accepted_at = models.DateTimeField(default=timezone.now)
    accepted_terms_version = models.CharField(max_length=6, default=get_current_terms_version)

    def __str__(self):
        return self.user.email