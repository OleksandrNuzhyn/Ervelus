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
            models.Index(fields=['user', 'is_visible', '-created_at'], name='user_visible_created_idx'),
            models.Index(fields=['user', '-created_at'], name='user_latest_req_idx'),
            models.Index(fields=['-created_at'], name='gen_req_created_at_desc_idx')
        ]

    class PrivacyMeta:
        fields = [
            'user',
            'input_img_url',
            'output_img_url',
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
                'chosen_style_name': instance.chosen_style.name,
                'input_img_url': instance.input_img_url,
                'output_img_url': instance.output_img_url,
                'input_thumb_url': instance.input_thumb_url,
                'input_large_url': instance.input_large_url,
                'output_thumb_url': instance.output_thumb_url,
                'output_large_url': instance.output_large_url,
                'output_original_url': instance.output_original_url,
                'status': instance.status,
                'error_message': instance.error_message,
                'is_hidden': instance.is_hidden,
                'is_visible': instance.is_visible,
                'created_at': instance.created_at,
                'updated_at': instance.updated_at
            }

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='generation_requests')
    chosen_style = models.ForeignKey('products.Style', on_delete=models.PROTECT, related_name='generation_requests')
    input_img_url = models.URLField(max_length=1024, null=True, blank=True)
    output_img_url = models.URLField(max_length=1024, null=True, blank=True)
    input_thumb_url = models.URLField(max_length=1024, null=True, blank=True)
    input_large_url = models.URLField(max_length=1024, null=True, blank=True)
    output_thumb_url = models.URLField(max_length=1024, null=True, blank=True)
    output_large_url = models.URLField(max_length=1024, null=True, blank=True)
    output_original_url = models.URLField(max_length=1024, null=True, blank=True)
    status = models.CharField(max_length=20, choices=GenerationStatus.choices, default=GenerationStatus.PROCESSING, db_index=True)
    error_message = models.TextField(null=True, blank=True)
    is_hidden = models.BooleanField(default=False)
    is_visible = models.BooleanField(default=False, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.chosen_style.name} - {self.user.email if self.user else 'No User'}"