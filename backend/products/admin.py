from django.contrib import admin
from django.db.models import Count
from .models import Style, Genre, StarPackage


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'generations_count')
    search_fields = ('name',)
    ordering = ('-id',)

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            generations_count=Count('styles__generation_requests')
        )
    
    @admin.display(ordering='generations_count', description='Generations count')
    def generations_count(self, obj):
        return obj.generations_count


@admin.register(Style)
class StyleAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'genre', 'is_paid', 'generations_count')
    list_filter = ('genre', 'is_paid')
    list_select_related = ('genre',)
    search_fields = ('name',)
    raw_id_fields = ('genre',)
    ordering = ('-id',)

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            generations_count=Count('generation_requests')
        )

    @admin.display(ordering='generations_count', description='Generations count')
    def generations_count(self, obj):
        return obj.generations_count


@admin.register(StarPackage)
class StarPackageAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'stars_count_t1', 'stars_count_t2', 'generations_count', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name',)
    ordering = ('generations_count',)