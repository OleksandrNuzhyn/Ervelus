from django.contrib import admin
from django.utils import timezone
from .models import GenerationRequest
from core.admin_mixins import NoLogAdminMixin


@admin.register(GenerationRequest)
class GenerationRequestAdmin(NoLogAdminMixin, admin.ModelAdmin):
    list_display = ('id', 'style_name', 'status', 'created_at_formatted', 'updated_at_formatted')
    list_select_related = ('chosen_style',)
    list_filter = ('status', 'created_at', 'chosen_style')
    search_fields = ('user__email', 'input_large_url', 'output_large_url')
    ordering = ('-id',)
    raw_id_fields = ('user', 'chosen_style')

    @admin.display(description='style')
    def style_name(self, obj):
        return obj.chosen_style.name if obj.chosen_style else "-"

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