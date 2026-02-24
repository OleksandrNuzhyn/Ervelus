from django.contrib import admin
from django.utils import timezone
from django.db.models import Count, Q
from .models import GenerationRequest
from core.admin_mixins import NoLogAdminMixin


@admin.register(GenerationRequest)
class GenerationRequestAdmin(NoLogAdminMixin, admin.ModelAdmin):
    list_display = ('id', 'style_name', 'status', 'type', 'created_at_formatted', 'updated_at_formatted')
    list_select_related = ('chosen_style',)
    list_filter = ('status', 'type', 'created_at', 'chosen_style')
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
        
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        from_time = request.GET.get('from_time')
        to_time = request.GET.get('to_time')
        
        if from_time:
            try:
                dt = timezone.datetime.fromisoformat(from_time)
                if timezone.is_naive(dt):
                    dt = timezone.make_aware(dt)
                qs = qs.filter(created_at__gte=dt)
            except (ValueError, TypeError):
                pass
        
        if to_time:
            try:
                dt = timezone.datetime.fromisoformat(to_time)
                if timezone.is_naive(dt):
                    dt = timezone.make_aware(dt)
                qs = qs.filter(created_at__lte=dt)
            except (ValueError, TypeError):
                pass
        
        return qs

    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(request, extra_context)
        if hasattr(response, 'context_data'):
            qs = response.context_data['cl'].queryset
            summary = qs.aggregate(
                total=Count('id'),
                completed_paid=Count('id', filter=Q(status=GenerationRequest.GenerationStatus.COMPLETED, type=GenerationRequest.CreditType.PAID)),
                completed_free=Count('id', filter=Q(status=GenerationRequest.GenerationStatus.COMPLETED, type=GenerationRequest.CreditType.FREE)),
                rejected=Count('id', filter=Q(status=GenerationRequest.GenerationStatus.REJECTED_BY_SAFETY)),
                failed=Count('id', filter=Q(status=GenerationRequest.GenerationStatus.FAILED)),
            )
            response.context_data['summary'] = summary
        return response