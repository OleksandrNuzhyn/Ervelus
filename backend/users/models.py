from django.db import models
from django.db.models import Q, Sum
from django.db.models.functions import Coalesce
from django.conf import settings


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

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='profile')
    paddle_customer_id = models.CharField(max_length=50, unique=True, null=True, blank=True)

    objects = UserProfileCreditManager()

    def __str__(self):
        return self.user.email