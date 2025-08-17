from django.contrib import admin
from django.db.models import Count
from .models import Style, SubscriptionPlan, Genre


@admin.register(SubscriptionPlan)
class SubscriptionPlanAdmin(admin.ModelAdmin):
    filter_horizontal = ('unlocked_styles',)


@admin.register(Style)
class StyleAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'genre', 'generation_count')
    list_select_related = ('genre',)

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.annotate(generation_count=Count("generation_requests")).order_by("-generation_count")
        return queryset

    def generation_count(self, obj):
        return obj.generation_count
    

admin.site.register(Genre)