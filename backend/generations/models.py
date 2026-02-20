from django.db import models
from django.conf import settings


class GenerationRequest(models.Model):
    class GenerationStatus(models.TextChoices):
        REJECTED_BY_SAFETY = 'rejected_by_safety'
        PROCESSING = 'processing'
        COMPLETED = 'completed'
        FAILED = 'failed'
    
    class Meta:
        verbose_name = 'Generation Request'
        verbose_name_plural = 'Generation Requests'
        indexes = [
            models.Index(fields=['user', 'status', '-created_at'], name='user_status_created_at_idx'),
            models.Index(fields=['user', '-created_at'], name='user_created_at_idx')
        ]

    class PrivacyMeta:
        fields = [
            'user',
            'input_thumb_url',
            'input_large_url',
            'output_thumb_url',
            'output_large_url',
            'output_original_url'
        ]
        search_fields = [
            'user__email',
        ]

        def export(self, instance):
            return {
                'chosen_style_name': instance.chosen_style.name if instance.chosen_style else None,
                'input_thumb_url': instance.input_thumb_url,
                'input_large_url': instance.input_large_url,
                'output_thumb_url': instance.output_thumb_url,
                'output_large_url': instance.output_large_url,
                'output_original_url': instance.output_original_url,
                'status': instance.status,
                'created_at': instance.created_at,
                'updated_at': instance.updated_at
            }

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='generation_requests')
    chosen_style = models.ForeignKey('products.Style', on_delete=models.SET_NULL, null=True, blank=True, related_name='generation_requests')
    status = models.CharField(max_length=20, choices=GenerationStatus.choices, default=GenerationStatus.PROCESSING)
    input_thumb_url = models.URLField(max_length=1024, null=True, blank=True)
    input_large_url = models.URLField(max_length=1024, null=True, blank=True)
    output_thumb_url = models.URLField(max_length=1024, null=True, blank=True)
    output_large_url = models.URLField(max_length=1024, null=True, blank=True)
    output_original_url = models.URLField(max_length=1024, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.chosen_style.name if self.chosen_style else 'Deleted Style'} - {self.user.email if self.user else 'No User'}"