from django.contrib.auth import get_user_model
from django.db import transaction
from django.utils.dateparse import parse_datetime
from products.models import SubscriptionPlan
from subscriptions.models import UserSubscription

User = get_user_model()

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