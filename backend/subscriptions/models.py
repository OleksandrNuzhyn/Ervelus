from django.db import models
from django.conf import settings


class UserSubscription(models.Model):
    class SubscriptionStatus(models.TextChoices):
        ACTIVE = 'active'
        INACTIVE = 'inactive'
        CANCELED = 'canceled'
        ABANDONED = 'abandoned'

    class Meta:
        verbose_name = 'User Subscription'
        verbose_name_plural = 'User Subscriptions'

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='subscriptions')
    plan = models.ForeignKey('products.SubscriptionPlan', on_delete=models.PROTECT, related_name='user_subscriptions')
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    status = models.CharField(max_length=20, choices=SubscriptionStatus.choices, default=SubscriptionStatus.ACTIVE)
    paddle_subscription_id = models.CharField(max_length=255, unique=True)
    remaining_credits = models.IntegerField()

    def __str__(self):
        return f'{self.user.email} - {self.plan.name}'