from django.db import models
from django.conf import settings
from django.utils import timezone
import uuid

def get_current_terms_version():
    return settings.CURRENT_TERMS_VERSION

class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile', editable=False)
    paddle_user_key = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    terms_accepted_at = models.DateTimeField(default=timezone.now)
    accepted_terms_version = models.CharField(default=get_current_terms_version)