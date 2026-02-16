from django.db import models
from django.conf import settings


class TermsVersion(models.Model):
    class DocumentType(models.TextChoices):
        TERMS_OF_SERVICE = 'terms_of_service', 'Terms of Service'
        PRIVACY_POLICY = 'privacy_policy', 'Privacy Policy'
        COOKIE_POLICY = 'cookie_policy', 'Cookie Policy'
        REFUND_POLICY = 'refund_policy', 'Refund Policy'

    class Meta:
        verbose_name = 'Terms Version'
        verbose_name_plural = 'Terms Versions'
        unique_together = ('document_type', 'version')
        indexes = [models.Index(fields=['-published_at'])]

    document_type = models.CharField(max_length=40, choices=DocumentType.choices)
    version = models.DecimalField(max_digits=10, decimal_places=2)
    content = models.TextField()
    published_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.get_document_type_display()} - v{self.version}'


class UserAgreement(models.Model):
    class Meta:
        verbose_name = 'User Agreement'
        verbose_name_plural = 'User Agreements'
        unique_together = ('user', 'terms_version')
        indexes = [
            models.Index(fields=['-accepted_at']),
            models.Index(fields=['ip_address'])
        ]

    class PrivacyMeta:
        fields = [
            'ip_address',
            'user_agent'
        ]
        search_fields = [
            'user__email',
        ]

        def export(self, instance):
            terms_version = instance.terms_version

            return {
                'terms_document_type': terms_version.get_document_type_display(),
                'terms_version': terms_version.version,
                'accepted_at': instance.accepted_at,
                'ip_address': instance.ip_address,
                'user_agent': instance.user_agent,
                'context': instance.context
            }

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='agreements')
    terms_version = models.ForeignKey(TermsVersion, on_delete=models.PROTECT, related_name='user_agreements')
    accepted_at = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(null=True, blank=True)
    context = models.JSONField(default=dict)

    def __str__(self):
        return f'{self.terms_version} - {self.user.email}'