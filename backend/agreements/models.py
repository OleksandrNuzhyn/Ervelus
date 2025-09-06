from django.db import models
from django.conf import settings


class TermsVersion(models.Model):
    class DocumentType(models.TextChoices):
        TERMS_OF_SERVICE = 'terms_of_service'
        PRIVACY_POLICY = 'privacy_policy'
        COOKIE_POLICY = 'cookie_policy'
        REFUND_POLICY = 'refund_policy'
        DMCA_POLICY = 'dmca_policy'
    
    # class HandlingType(models.TextChoices):
    #     REQUIRES_ACCEPTANCE = 'requires_acceptance', 'Requires Acceptance'
    #     INFORMATIONAL = 'informational', 'Informational'
    #     INCORPORATED = 'incorporated', 'Incorporated into ToS'

    class Meta:
        verbose_name = 'Terms Version'
        verbose_name_plural = 'Terms Versions'
        unique_together = ('document_type', 'version')

    document_type = models.CharField(max_length=40, choices=DocumentType.choices)
    version = models.DecimalField(max_digits=10, decimal_places=2)
    content = models.TextField()
    published_at = models.DateTimeField(auto_now_add=True)
    # handling_type = models.CharField(
    #     max_length=30, 
    #     choices=HandlingType.choices,
    #     default=HandlingType.REQUIRES_ACCEPTANCE
    # )

    def __str__(self):
        return f'{self.get_document_type_display()} - v{self.version}'


class UserAgreement(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='agreements')
    terms_version = models.ForeignKey('agreements.TermsVersion', on_delete=models.PROTECT, related_name='user_agreements')
    accepted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'User Agreement'
        verbose_name_plural = 'User Agreements'
        unique_together = ('user', 'terms_version')

    def __str__(self):
        return f'{self.user} accepted {self.terms_version}'