from django.contrib import admin
from django.utils import timezone
from django.db.models import Count, Q
from .models import GenerationRequest
from core.admin_mixins import NoLogAdminMixin
from rangefilter.filters import DateTimeRangeFilter


@admin.register(GenerationRequest)
class GenerationRequestAdmin(NoLogAdminMixin, admin.ModelAdmin):
    list_display = ('id', 'style_name', 'status', 'type', 'created_at_formatted', 'updated_at_formatted')
    list_select_related = ('chosen_style',)
    list_filter = (
        ('created_at', DateTimeRangeFilter),
        'status',
        'type',
        ('chosen_style', admin.RelatedOnlyFieldListFilter)
    )
    search_fields = ('user__email', 'input_large_url', 'output_large_url')
    ordering = ('-id',)
    raw_id_fields = ('user', 'chosen_style')
    readonly_fields = ('created_at_formatted', 'updated_at_formatted')

    @admin.display(description='style')
    def style_name(self, obj):
        return obj.chosen_style.name if obj.chosen_style else "-"

    @admin.display(ordering='created_at', description='created at')
    def created_at_formatted(self, obj):
        return timezone.localtime(obj.created_at).strftime('%d.%m.%Y %H:%M:%S')

    @admin.display(ordering='updated_at', description='updated at')
    def updated_at_formatted(self, obj):
        return timezone.localtime(obj.updated_at).strftime('%d.%m.%Y %H:%M:%S')

    def has_add_permission(self, request):
        return False

    def changelist_view(self, request, extra_context=None):
        queryset = self.get_changelist_instance(request).get_queryset(request)
        
        statistics = queryset.aggregate(
            total=Count('id'),
            free=Count('id', filter=Q(status='completed', type='free')),
            paid=Count('id', filter=Q(status='completed', type='paid')),
            completed=Count('id', filter=Q(status='completed')),
            rejected=Count('id', filter=Q(status='rejected_by_safety')),
            failed=Count('id', filter=Q(status='failed'))
        )
        
        extra_context = extra_context or {}
        extra_context['statistics'] = statistics

        return super().changelist_view(request, extra_context=extra_context)