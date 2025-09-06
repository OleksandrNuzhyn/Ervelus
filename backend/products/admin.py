from django.contrib import admin
from django.db.models import Count
from .models import Style, SubscriptionPlan, Genre


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'generation_count')

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.annotate(generation_count=Count("styles__generation_requests")).order_by("-generation_count")
        return queryset

    def generation_count(self, obj):
        return obj.generation_count


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


@admin.register(SubscriptionPlan)
class SubscriptionPlanAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'purchase_count')
    filter_horizontal = ('unlocked_styles',)

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.annotate(purchase_count=Count("user_subscriptions")).order_by("-purchase_count")
        return queryset

    def purchase_count(self, obj):
        return obj.purchase_count