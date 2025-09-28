import requests
from django.utils import timezone
from django.conf import settings
from django.contrib import admin, messages
from .models import UserSubscription
from core.admin_mixins import NoLogAdminMixin

@admin.action(description="Cancel selected subscriptions at the next billing period")
def cancel_subscription_at_next_billing_period(modeladmin, request, queryset):
    headers = {
        "Authorization": f"Bearer {settings.PADDLE_API_KEY}",
        "Content-Type": "application/json",
    }
    success_count = 0
    failed_ids = []

    for subscription in queryset:
        url = f"{settings.PADDLE_API_BASE_URL}/subscriptions/{subscription.paddle_subscription_id}/cancel"

        try:
            response = requests.post(url, headers=headers)
            response.raise_for_status()
            success_count += 1
        except requests.RequestException:
            failed_ids.append(subscription.paddle_subscription_id)

    if success_count:
        modeladmin.message_user(request, f"Successfully scheduled cancellation for {success_count} subscriptions", messages.SUCCESS)
    if failed_ids:
        modeladmin.message_user(request, f"Failed to schedule cancellation for {len(failed_ids)} subscriptions: {', '.join(failed_ids)}", messages.ERROR)


@admin.register(UserSubscription)
class UserSubscriptionAdmin(NoLogAdminMixin, admin.ModelAdmin):
    list_display = ("id", "user__email", "plan__name", "status", "remaining_credits", "start_time_formatted", "end_time_formatted")
    list_select_related = ("user", "plan")
    list_filter = ("plan__name", "status", 'start_time', 'end_time', 'cancels_at')
    search_fields = ("user__email", "plan__name", "paddle_subscription_id")
    ordering = ("-id",)
    raw_id_fields = ("user", "plan")
    actions = [cancel_subscription_at_next_billing_period]

    @admin.display(ordering='start_time', description='start time')
    def start_time_formatted(self, obj):
        return timezone.localtime(obj.start_time).strftime('%d.%m.%Y %H:%M:%S')

    @admin.display(ordering='end_time', description='end time')
    def end_time_formatted(self, obj):
        return timezone.localtime(obj.end_time).strftime('%d.%m.%Y %H:%M:%S')