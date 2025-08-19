from django.contrib import admin
from .models import UserSubscription


@admin.register(UserSubscription)
class UserSubscriptionAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'plan', 'status', 'remaining_credits', 'end_time')
    list_select_related = ('user', 'plan')
    list_filter = ('status', 'end_time')
    search_fields = ('paddle_subscription_id',)