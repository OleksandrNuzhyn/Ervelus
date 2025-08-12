from django.contrib import admin
from .models import Style, SubscriptionPlan, Genre


@admin.register(SubscriptionPlan)
class SubscriptionPlanAdmin(admin.ModelAdmin):
    filter_horizontal = ('unlocked_styles',)


@admin.register(Style)
class StyleAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'genre')
    list_select_related = ('genre',)


admin.site.register(Genre)