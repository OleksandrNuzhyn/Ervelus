from django.db import models
from django.conf import settings
from django.utils import timezone
from auditlog.registry import auditlog


class UserSubscription(models.Model):
    class Meta:
        verbose_name = 'User Subscription'
        verbose_name_plural = 'User Subscriptions'
        indexes = [
            models.Index(fields=['user', 'end_time', 'remaining_credits'], name='user_end_time_credits_idx'),
            models.Index(fields=['user', 'is_auto_renew'], name='user_auto_renew_idx')
        ]
        
    class PrivacyMeta:
        can_anonymise = False
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
                'is_auto_renew': instance.is_auto_renew,
                'rec_token': instance.rec_token,
                'order_reference': instance.order_reference,
                'remaining_credits': instance.remaining_credits
            }

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='subscriptions')
    plan = models.ForeignKey('products.SubscriptionPlan', on_delete=models.PROTECT, related_name='user_subscriptions')
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(db_index=True)
    is_auto_renew = models.BooleanField(default=True)
    rec_token = models.CharField(max_length=255, null=True, blank=True)
    order_reference = models.CharField(max_length=255, unique=True)
    remaining_credits = models.IntegerField()
    
    @property
    def display_status(self):
        now = timezone.now()
        
        if self.end_time > now:
            if self.is_auto_renew:
                return f"Active"
            return f"Active until {self.end_time.strftime('%B %d, %Y')}"
        elif self.is_auto_renew:
            return "Past Due"
            
        return "Canceled"
    
    def __str__(self):
        return f'{self.plan.name} - {self.user.email}'


auditlog.register(UserSubscription)