from django.utils import timezone
from django.contrib import admin
from .models import UserSubscription
from core.admin_mixins import NoLogAdminMixin
from django.contrib import messages
from . import services

@admin.action(description='Cancel selected subscriptions')
def cancel_subscription_action(modeladmin, request, queryset):
    success_count = 0
    fail_count = 0
    
    for subscription in queryset:
        if services.cancel_subscription(subscription):
            success_count += 1
        else:
            fail_count += 1
            
    if success_count:
        modeladmin.message_user(request, f"Successfully cancelled {success_count} subscriptions", messages.SUCCESS)
    if fail_count:
        modeladmin.message_user(request, f"Failed to cancel {fail_count} subscriptions", messages.ERROR)


@admin.register(UserSubscription)
class UserSubscriptionAdmin(NoLogAdminMixin, admin.ModelAdmin):
    list_display = ("id", "user__email", "plan__name", "is_auto_renew", "remaining_credits", "start_time_formatted", "end_time_formatted")
    list_select_related = ("user", "plan")
    list_filter = ("plan__name", "is_auto_renew", 'start_time', 'end_time')
    search_fields = ("user__email", "plan__name", "order_reference")
    ordering = ("-id",)
    raw_id_fields = ("user", "plan")
    actions = [cancel_subscription_action]

    @admin.display(ordering='start_time', description='start time')
    def start_time_formatted(self, obj):
        return timezone.localtime(obj.start_time).strftime('%d.%m.%Y %H:%M:%S')

    @admin.display(ordering='end_time', description='end time')
    def end_time_formatted(self, obj):
        return timezone.localtime(obj.end_time).strftime('%d.%m.%Y %H:%M:%S')