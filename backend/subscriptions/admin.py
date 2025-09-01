import requests
from django.conf import settings
from django.contrib import admin, messages
from .models import UserSubscription

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
class UserSubscriptionAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "plan", "status", "remaining_credits", "end_time")
    list_select_related = ("user", "plan")
    list_filter = ("status", "end_time")
    search_fields = ("paddle_subscription_id",)
    actions = [cancel_subscription_at_next_billing_period]