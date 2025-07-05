from django.db import models
from django.conf import settings
import uuid


class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile', editable=False)
    paddle_user_key = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
