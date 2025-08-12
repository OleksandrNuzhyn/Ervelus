from django.db import models
from django.conf import settings
from django.core.validators import URLValidator


class GenerationRequest(models.Model):
    class GenerationStatus(models.TextChoices):
        PROCESSING = 'processing'
        COMPLETED = 'completed'
        FAILED = 'failed'
    
    class Meta:
        verbose_name = 'Generation Request'
        verbose_name_plural = 'Generation Requests'
        indexes = [
            models.Index(fields=['user', 'status', '-created_at'], name='user_status_created_at_idx')
        ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='generation_requests')
    chosen_style = models.ForeignKey('products.Style', on_delete=models.PROTECT, related_name='generation_requests')
    input_img_url = models.TextField(validators=[URLValidator()])
    output_img_url = models.TextField(blank=True, null=True, validators=[URLValidator()])
    status = models.CharField(max_length=20, choices=GenerationStatus.choices, default=GenerationStatus.PROCESSING, db_index=True)
    error_message = models.TextField(blank=True, null=True)
    error_api_message = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.email}"