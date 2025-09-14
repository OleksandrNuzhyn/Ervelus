from django.db import models
from django.db.models import Q
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
        indexes = [
            models.Index(fields=['user', 'status'], name='user_status_idx'),
            models.Index(
                fields=['user', 'end_time'],
                name='user_active_credits_end_idx',
                condition=Q(status='active', remaining_credits__gt=0),
            )
        ]

    class PrivacyMeta:
        fields = []
        search_fields = [
            'user__email',
        ]

        def export(self, instance):
            plan = instance.plan
            unlocked_styles = ', '.join([style.name for style in plan.unlocked_styles.all()])

            return {
                'plan_name': plan.name,
                'plan_description': plan.description,
                'plan_price': plan.price,
                'plan_features': plan.features,
                'plan_unlocked_styles': unlocked_styles,
                'plan_generations_count': plan.generations_count,
                'start_time': instance.start_time,
                'end_time': instance.end_time,
                'status': instance.status,
                'cancels_at': instance.cancels_at,
                'paddle_subscription_id': instance.paddle_subscription_id,
                'remaining_credits': instance.remaining_credits,
            }

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='subscriptions')
    plan = models.ForeignKey('products.SubscriptionPlan', on_delete=models.PROTECT, related_name='user_subscriptions')
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    status = models.CharField(max_length=20, choices=SubscriptionStatus.choices, default=SubscriptionStatus.ACTIVE, db_index=True)
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
                return f"Active until {self.cancels_at.strftime('%b %d, %Y')}"
            
            return "Cancellation Processing"
        
        if self.status == self.SubscriptionStatus.PAST_DUE:
            return f"Payment issue. Please update your payment method by {self.end_time.strftime('%b %d, %Y')}"
            
        if self.status == self.SubscriptionStatus.CANCELED:
            return "Canceled"
            
        return "Unknown"