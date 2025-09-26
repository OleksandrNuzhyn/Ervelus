from django.contrib import admin
from django.utils import timezone
from .models import GenerationRequest
from core.admin_mixins import NoLogAdminMixin


@admin.register(GenerationRequest)
class GenerationRequestAdmin(NoLogAdminMixin, admin.ModelAdmin):
    list_display = ('id', 'user__email', 'status', 'created_at_formatted')
    list_select_related = ('user',)
    list_filter = ('status', 'created_at', 'is_hidden', 'chosen_style__name')
    search_fields = ('user__email', 'input_img_url', 'output_img_url')
    ordering = ('-created_at',)
    raw_id_fields = ('user', 'chosen_style')

    @admin.display(ordering='created_at', description='created at')
    def created_at_formatted(self, obj):
        return timezone.localtime(obj.created_at).strftime('%d.%m.%Y %H:%M:%S')

    @admin.display(ordering='updated_at', description='updated at')
    def updated_at_formatted(self, obj):
        return timezone.localtime(obj.updated_at).strftime('%d.%m.%Y %H:%M:%S')

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ('created_at_formatted', 'updated_at_formatted')
        else:
            return ()