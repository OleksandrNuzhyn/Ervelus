from django.contrib import admin
from .models import Style, SubscriptionPlan, Genre


class SubscriptionPlanAdmin(admin.ModelAdmin):
    filter_horizontal = ('unlocked_styles',)


admin.site.register(Style)
admin.site.register(SubscriptionPlan, SubscriptionPlanAdmin)
admin.site.register(Genre)