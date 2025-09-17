from django.db import models
from django.conf import settings
from django.core.validators import URLValidator


class GenerationRequest(models.Model):
    class GenerationStatus(models.TextChoices):
        PROCESSING = 'processing'
        COMPLETED = 'completed'
        FAILED = 'failed'
        STOPPED_BY_USER = 'stopped_by_user'
        REJECTED_BY_SAFETY = 'rejected_by_safety'
    
    class Meta:
        verbose_name = 'Generation Request'
        verbose_name_plural = 'Generation Requests'
        indexes = [
            models.Index(fields=['user', 'status', 'is_hidden', '-created_at'], name='u_s_ih_ca_idx')
        ]

    class PrivacyMeta:
        fields = [
            'user',
            'input_img_url',
            'output_img_url'
        ]
        search_fields = [
            'user__email',
        ]

        def export(self, instance):
            return {
                'chosen_style_name': instance.chosen_style.name,
                'input_img_url': instance.input_img_url,
                'output_img_url': instance.output_img_url,
                'status': instance.status,
                'error_message': instance.error_message,
                'error_api_message': instance.error_api_message,
                'is_hidden': instance.is_hidden,
                'created_at': instance.created_at,
                'updated_at': instance.updated_at
            }

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='generation_requests')
    chosen_style = models.ForeignKey('products.Style', on_delete=models.PROTECT, related_name='generation_requests')
    input_img_url = models.TextField(validators=[URLValidator()], null=True, blank=True)
    output_img_url = models.TextField(validators=[URLValidator()], null=True, blank=True)
    status = models.CharField(max_length=20, choices=GenerationStatus.choices, default=GenerationStatus.PROCESSING, db_index=True)
    error_message = models.TextField(null=True, blank=True)
    error_api_message = models.TextField(null=True, blank=True)
    is_hidden = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.email}"