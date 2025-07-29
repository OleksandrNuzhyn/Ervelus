from asgiref.sync import sync_to_async
from django.contrib.auth import get_user_model
from django.db import transaction
from django.utils.dateparse import parse_datetime
from products.models import SubscriptionPlan
from subscriptions.models import UserSubscription
from django.conf import settings
from users.models import UserProfile
import httpx

User = get_user_model()

@sync_to_async()
def handle_subscription_activated(data):
    try:
        user_id = data.get('custom_data').get('user_id')
        paddle_customer_id = data.get('customer_id')
        paddle_subscription_id = data.get('id')

        with transaction.atomic():
            user = User.objects.select_for_update().get(id=user_id)

            if not user.profile.paddle_customer_id:
                user.profile.paddle_customer_id = paddle_customer_id
                user.profile.save(update_fields=['paddle_customer_id'])

            paddle_price_id = data['items'][0]['price']['id']
            plan = SubscriptionPlan.objects.get(paddle_price_id=paddle_price_id)

            UserSubscription.objects.create(
                user=user,
                plan=plan,
                start_time=parse_datetime(data['first_billed_at']),
                end_time=parse_datetime(data['next_billed_at']),
                status=UserSubscription.SubscriptionStatus.ACTIVE,
                paddle_subscription_id=paddle_subscription_id,
                remaining_credits=plan.generations_count
            )
    except Exception:
        raise Exception()

async def create_customer_portal_session(user):
    profile = await UserProfile.objects.aget(user=user)

    if not profile.paddle_customer_id:
        raise Exception()

    paddle_customer_id = profile.paddle_customer_id
    url = f"https://sandbox-api.paddle.com/customers/{paddle_customer_id}/portal-sessions"
    headers = {
        "Authorization": f"Bearer {settings.PADDLE_API_KEY}",
        "Content-Type": "application/json",
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(url, headers=headers)
            response.raise_for_status()
        except httpx.HTTPStatusError:
            raise Exception()

    response_data = response.json()
    return response_data['data']['urls']['general']['overview']