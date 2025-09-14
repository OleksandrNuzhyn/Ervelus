from django.contrib import admin
from .models import TermsVersion, UserAgreement
from core.admin_mixins import NoLogAdminMixin


@admin.register(TermsVersion)
class TermsVersionAdmin(admin.ModelAdmin):
    list_display = ('document_type', 'version', 'published_at')
    list_filter = ('document_type',)


@admin.register(UserAgreement)
class UserAgreementAdmin(NoLogAdminMixin, admin.ModelAdmin):
    list_display = ('user', 'terms_version', 'accepted_at')
    list_filter = ('terms_version__document_type',)