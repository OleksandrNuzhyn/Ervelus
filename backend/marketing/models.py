from django.db import models
from django.conf import settings


class PromoCode(models.Model):
    class Meta:
        verbose_name = "Promo Code"
        verbose_name_plural = "Promo Codes"

    code = models.CharField(max_length=50, unique=True)
    description = models.TextField(null=True, blank=True)
    credits_count = models.PositiveIntegerField()
    max_usages = models.PositiveIntegerField()
    current_usages = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.code


class PromoCodeUsage(models.Model):
    class Meta:
        verbose_name = "Promo Code Usage"
        verbose_name_plural = "Promo Code Usages"
        unique_together = ('user', 'promo_code')

    class PrivacyMeta:
        fields = [
            'user',
        ]
        search_fields = [
            'user__email',
        ]

        def export(self, instance):
            return {
                'promo_code': instance.promo_code.code,
                'used_at': instance.used_at
            }

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='promo_code_usages')
    promo_code = models.ForeignKey(PromoCode, on_delete=models.CASCADE, related_name='usages')
    used_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email if self.user else 'No User'} - {self.promo_code.code}"