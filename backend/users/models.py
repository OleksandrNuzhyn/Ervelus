from django.db import models
from django.db.models import Q, Sum
from django.db.models.functions import Coalesce
from django.conf import settings
from django.utils import timezone

def get_current_terms_version():
    return settings.CURRENT_TERMS_VERSION


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

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile', editable=False)
    paddle_customer_id = models.CharField(max_length=50, unique=True, null=True, blank=True)
    terms_accepted_at = models.DateTimeField(default=timezone.now)
    accepted_terms_version = models.CharField(max_length=6, default=get_current_terms_version)

    objects = UserProfileCreditManager()

    def __str__(self):
        return self.user.email