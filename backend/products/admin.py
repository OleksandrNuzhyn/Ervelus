from django.contrib import admin
from django.db.models import Count
from .models import Style, SubscriptionPlan, Genre


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'generation_count')
    search_fields = ('name',)

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.annotate(generation_count=Count("styles__generation_requests")).order_by("-generation_count")
        return queryset

    def generation_count(self, obj):
        return obj.generation_count


@admin.register(Style)
class StyleAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'genre', 'generation_count')
    list_filter = ('genre',)
    list_select_related = ('genre',)
    search_fields = ('name',)
    raw_id_fields = ('genre',)

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.annotate(generation_count=Count("generation_requests")).order_by("-generation_count")
        return queryset

    def generation_count(self, obj):
        return obj.generation_count


@admin.register(SubscriptionPlan)
class SubscriptionPlanAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'generations_count', 'is_active', 'product_price', 'purchase_count')
    list_filter = ('is_active',)
    search_fields = ('name', 'description', 'paddle_price_id', 'features')
    filter_horizontal = ('unlocked_styles',)

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.annotate(purchase_count=Count("user_subscriptions")).order_by("-purchase_count")
        return queryset

    def purchase_count(self, obj):
        return obj.purchase_count