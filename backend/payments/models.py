from django.db import models
from django.conf import settings


class UserPurchase(models.Model):
    class Meta:
        verbose_name = 'User Purchase'
        verbose_name_plural = 'User Purchases'

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='purchases')
    stars_count = models.IntegerField()
    generations_count = models.IntegerField()
    purchased_at = models.DateTimeField(auto_now_add=True)
    transaction_id = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return f"Purchase ({self.stars_count} stars)"