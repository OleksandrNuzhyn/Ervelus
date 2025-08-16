from django.db import models
from django.conf import settings
from django.utils import timezone


class UserSubscription(models.Model):
    class SubscriptionStatus(models.TextChoices):
        ACTIVE = 'active'
        PAST_DUE = 'past_due'
        CANCELED = 'canceled'

    class Meta:
        verbose_name = 'User Subscription'
        verbose_name_plural = 'User Subscriptions'

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='subscriptions')
    plan = models.ForeignKey('products.SubscriptionPlan', on_delete=models.PROTECT, related_name='user_subscriptions')
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    status = models.CharField(max_length=20, choices=SubscriptionStatus.choices, default=SubscriptionStatus.ACTIVE)
    cancels_at = models.DateTimeField(null=True, blank=True)
    paddle_subscription_id = models.CharField(max_length=255, unique=True)
    remaining_credits = models.IntegerField()

    def __str__(self):
        return f'{self.user.email} - {self.plan.name}'
    
    @property
    def display_status(self):
        now = timezone.now()
    
        if self.status == self.SubscriptionStatus.ACTIVE:
            if not self.cancels_at:
                return "Active"
            
            if self.cancels_at > now:
                return f'Active until {self.cancels_at.strftime("%b %d, %Y")}'
            
            return "Cancellation Processing"
        
        if self.status == self.SubscriptionStatus.PAST_DUE:
            return "Payment Failed"
            
        if self.status == self.SubscriptionStatus.CANCELED:
            return "Canceled"
            
        return "Unknown"