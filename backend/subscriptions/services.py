import datetime
from django.contrib.auth import get_user_model
from django.db import transaction
from django.utils.dateparse import parse_datetime
from django.utils import timezone
from dateutil.relativedelta import relativedelta
from django.conf import settings
from products.models import SubscriptionPlan
from subscriptions.models import UserSubscription
import requests

User = get_user_model()

def handle_transaction_completed(data):
    origin = data.get('origin')

    if origin == 'web':
        create_new_subscription(data)
    elif origin == 'subscription_recurring':
        renew_subscription(data)
    elif origin == 'subscription_payment_method_change':
        pass
    else:
        raise Exception()

def create_new_subscription(data):
    try:
        user_id = data.get('custom_data').get('user_id')
        paddle_customer_id = data.get('customer_id')
        paddle_subscription_id = data.get('subscription_id')

        if UserSubscription.objects.filter(paddle_subscription_id=paddle_subscription_id).exists():
            return

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
                start_time=parse_datetime(data.get('billing_period').get('starts_at')),
                end_time=parse_datetime(data.get('billing_period').get('ends_at')),
                status=UserSubscription.SubscriptionStatus.ACTIVE,
                paddle_subscription_id=paddle_subscription_id,
                remaining_credits=plan.generations_count
            )
    except Exception:
        raise Exception()

def renew_subscription(data):
    paddle_subscription_id = data.get('subscription_id')

    try:
        with transaction.atomic():
            user_subscription = (
                UserSubscription.objects.select_for_update()
                .select_related('plan')
                .get(paddle_subscription_id=paddle_subscription_id)
            )

            if user_subscription.status == UserSubscription.SubscriptionStatus.ACTIVE:
                user_subscription.end_time = parse_datetime(data.get('billing_period').get('ends_at'))
                user_subscription.remaining_credits = user_subscription.plan.generations_count

                user_subscription.save(update_fields=['end_time', 'remaining_credits'])
            elif user_subscription.status == UserSubscription.SubscriptionStatus.PAST_DUE:
                user_subscription.status = UserSubscription.SubscriptionStatus.ACTIVE
                user_subscription.end_time = timezone.now() + relativedelta(months=1)
                user_subscription.remaining_credits = user_subscription.plan.generations_count
                
                user_subscription.save(update_fields=['status', 'end_time', 'remaining_credits'])
                update_paddle_billing_period_ends_time(paddle_subscription_id, user_subscription.end_time)
            else:
                raise Exception()
    except Exception:
        raise Exception()

def format_datetime_for_paddle(datetime_object):
    if timezone.is_naive(datetime_object):
        datetime_object = timezone.make_aware(datetime_object, timezone.utc)
    
    utc_time = datetime_object.astimezone(datetime.timezone.utc)
    
    return utc_time.isoformat(timespec='seconds').replace('+00:00', 'Z')

def update_paddle_billing_period_ends_time(paddle_subscription_id, end_time):
    try:
        url = f"{settings.PADDLE_API_BASE_URL.rstrip('/')}/subscriptions/{paddle_subscription_id}"
        headers = {
            'Authorization': f"Bearer {settings.PADDLE_API_KEY}",
            'Content-Type': 'application/json'
        }
        payload = {
            'next_billed_at': format_datetime_for_paddle(end_time),
            'proration_billing_mode': 'do_not_bill'
        }

        response = requests.patch(url, json=payload, headers=headers)
        response.raise_for_status()
    except Exception:
        raise Exception()

def handle_transaction_past_due(data):
    paddle_subscription_id = data.get('subscription_id')

    try:
        user_subscription = UserSubscription.objects.get(paddle_subscription_id=paddle_subscription_id)
        user_subscription.status = UserSubscription.SubscriptionStatus.PAST_DUE
        user_subscription.end_time = parse_datetime(data.get('billing_period').get('ends_at'))
        user_subscription.save(update_fields=['status', 'end_time'])
    except Exception:
        raise Exception()
    
def handle_subscription_updated(data):
    paddle_subscription_id = data.get('id')
    status = data.get('status')
    scheduled_change = data.get('scheduled_change')

    try:
        user_subscription = UserSubscription.objects.get(paddle_subscription_id=paddle_subscription_id)

        if status == 'active' and not scheduled_change:
            if user_subscription.cancels_at is not None:
                user_subscription.cancels_at = None
                user_subscription.save(update_fields=['cancels_at'])
            else:
                return
        elif status == 'active' and scheduled_change and scheduled_change.get('action') == 'cancel':
            user_subscription.cancels_at = parse_datetime(scheduled_change.get('effective_at'))
            user_subscription.save(update_fields=['cancels_at'])
            return
        elif status == 'past_due':
            return
        elif status == 'canceled':
            return    
        else:
            raise Exception()
    except Exception:
        raise Exception()

def handle_subscription_canceled(data):
    paddle_subscription_id = data.get('id')

    try:
        user_subscription = UserSubscription.objects.get(paddle_subscription_id=paddle_subscription_id)
        user_subscription.status = UserSubscription.SubscriptionStatus.CANCELED
        user_subscription.cancels_at = None
        user_subscription.save(update_fields=['status', 'cancels_at'])
    except Exception:
        raise Exception()