from django.contrib import admin
from django.utils import timezone
from .models import GenerationRequest


@admin.register(GenerationRequest)
class GenerationRequestAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'status',
        'created_at_formatted',
        'updated_at_formatted',
    )
    list_select_related = ('user',)
    readonly_fields = (
        'created_at_formatted',
        'updated_at_formatted',
    )
    list_filter = ('status', 'created_at')

    @admin.display(ordering='created_at', description='created at')
    def created_at_formatted(self, obj):
        return timezone.localtime(obj.created_at).strftime('%Y-%m-%d %H:%M:%S')

    @admin.display(ordering='updated_at', description='updated at')
    def updated_at_formatted(self, obj):
        return timezone.localtime(obj.updated_at).strftime('%Y-%m-%d %H:%M:%S')