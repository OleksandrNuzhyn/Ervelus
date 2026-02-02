from django.urls import path
from django.contrib import admin
from django.db.models import Count
from django.template.response import TemplateResponse
from .models import Style, StarPackage, Genre


class StatisticsAdminMixin:
    statistics_annotation_lookup = None
    statistics_header = None

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('statistics/', self.admin_site.admin_view(self.statistics_view), name='statistics')
        ]
        
        return custom_urls + urls

    def statistics_view(self, request):
        selected_ids = request.GET.get('ids', '').split(',')
        if not all(item.isdigit() for item in selected_ids if item):
            selected_ids = []

        queryset = self.model.objects.filter(id__in=selected_ids).annotate(
            statistics_count=Count(self.statistics_annotation_lookup)
        ).order_by('-statistics_count')

        context = self.admin_site.each_context(request)
        context['opts'] = self.model._meta
        verbose_name_plural_formatted = " ".join([word.capitalize() for word in self.model._meta.verbose_name_plural.split(' ')])
        context['title'] = f'Statistics for selected {verbose_name_plural_formatted}'
        context['results'] = queryset
        context['statistics_header'] = self.statistics_header
        
        return TemplateResponse(request, 'admin/statistics.html', context)


@admin.register(Genre)
class GenreAdmin(StatisticsAdminMixin, admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)
    ordering = ('-id',)
    change_list_template = 'admin/products/genre/change_list.html'
    statistics_annotation_lookup = 'styles__generation_requests'
    statistics_header = 'Generation Count'


@admin.register(Style)
class StyleAdmin(StatisticsAdminMixin, admin.ModelAdmin):
    list_display = ('id', 'name', 'genre')
    list_filter = ('genre',)
    list_select_related = ('genre',)
    search_fields = ('name',)
    raw_id_fields = ('genre',)
    ordering = ('-id',)
    change_list_template = 'admin/products/style/change_list.html'
    statistics_annotation_lookup = 'generation_requests'
    statistics_header = 'Generation Count'


@admin.register(StarPackage)
class StarPackageAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'stars_count_t1', 'stars_count_t2', 'generations_count', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name',)
    ordering = ('generations_count',)