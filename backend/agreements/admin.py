from django.contrib import admin
from django.utils import timezone
from .models import TermsVersion, UserAgreement
from core.admin_mixins import NoLogAdminMixin


@admin.register(TermsVersion)
class TermsVersionAdmin(admin.ModelAdmin):
    list_display = ('id', 'document_type', 'version', 'published_at_formatted')
    list_filter = ('document_type', 'version', 'published_at')
    search_fields = ('content',)
    ordering = ('-published_at',)

    @admin.display(ordering='published_at', description='published at')
    def published_at_formatted(self, obj):
        return timezone.localtime(obj.published_at).strftime('%d.%m.%Y %H:%M:%S')


@admin.register(UserAgreement)
class UserAgreementAdmin(NoLogAdminMixin, admin.ModelAdmin):
    list_display = ('id', 'user__email', 'terms_version', 'accepted_at_formatted')
    list_filter = ('terms_version__document_type', 'terms_version__version', 'accepted_at')
    list_select_related = ('user', 'terms_version')
    search_fields = ('user__email', 'ip_address', 'user_agent')
    ordering = ('-accepted_at',)

    @admin.display(ordering='accepted_at', description='accepted at')
    def accepted_at_formatted(self, obj):
        return timezone.localtime(obj.accepted_at).strftime('%d.%m.%Y %H:%M:%S')
    
    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ('user', 'terms_version', 'accepted_at_formatted', 'ip_address', 'user_agent', 'context')
        else:
            return ()
        
    def has_add_permission(self, request):
        return False
    
    def has_delete_permission(self, request, obj=None):
        return False