import datetime
import logging
from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import F
from django.utils.dateparse import parse_datetime
from django.utils import timezone
from dateutil.relativedelta import relativedelta
from django.conf import settings
from products.models import SubscriptionPlan
from subscriptions.models import UserSubscription
from core.models import ApplicationConfig
import requests

User = get_user_model()
logger = logging.getLogger(__name__)

def handle_transaction_completed(data):
    origin = data.get('origin')
    paddle_subscription_id = data.get('subscription_id')

    if origin == 'web':
        create_new_subscription(data)
    elif origin == 'subscription_recurring':
        renew_subscription(data)
    elif origin == 'subscription_payment_method_change':
        logger.info("Skipping payment method change", extra={'paddle_subscription_id': paddle_subscription_id})
    else:
        logger.error("Unhandled origin", extra={'paddle_data': data})

def create_new_subscription(data):
    paddle_subscription_id = data.get('subscription_id')
    user_id = data.get('custom_data', {}).get('user_id')
    paddle_customer_id = data.get('customer_id')
    
    try:
        if UserSubscription.objects.filter(paddle_subscription_id=paddle_subscription_id).exists():
            logger.error("Subscription already exists, skipping creation", extra={'paddle_data': data})
            return

        with transaction.atomic():
            user = User.objects.select_for_update().get(id=user_id)

            if not user.profile.paddle_customer_id:
                user.profile.paddle_customer_id = paddle_customer_id
                user.profile.save(update_fields=['paddle_customer_id'])
                logger.info("Successfully updated user's paddle customer id", extra={'user_id': user_id, 'paddle_customer_id': paddle_customer_id})

            paddle_price_id = data['items'][0]['price']['id']
            plan = SubscriptionPlan.objects.select_for_update().get(paddle_price_id=paddle_price_id)

            if not plan.is_active:
                logger.warning("Attempted to create a subscription for an INACTIVE plan", extra={'paddle_data': data, 'plan_id': plan.id})

            UserSubscription.objects.create(
                user=user,
                plan=plan,
                start_time=parse_datetime(data.get('billing_period').get('starts_at')),
                end_time=parse_datetime(data.get('billing_period').get('ends_at')),
                status=UserSubscription.SubscriptionStatus.ACTIVE,
                paddle_subscription_id=paddle_subscription_id,
                remaining_credits=plan.generations_count
            )
            
            config = ApplicationConfig.objects.select_for_update().get_solo()
            config.reserved_for_spend = F('reserved_for_spend') + plan.product_price
            config.save(update_fields=['reserved_for_spend'])
            
            logger.info("Successfully created new subscription", extra={'user_id': user_id, 'paddle_subscription_id': paddle_subscription_id})
    except Exception as e:
        logger.error("Failed to create new subscription", extra={'paddle_data': data, 'error': str(e)}, exc_info=True)

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
                logger.info("Successfully renewed active subscription", extra={'paddle_subscription_id': paddle_subscription_id})
            elif user_subscription.status == UserSubscription.SubscriptionStatus.PAST_DUE:
                user_subscription.status = UserSubscription.SubscriptionStatus.ACTIVE
                user_subscription.end_time = timezone.now() + relativedelta(months=1)
                user_subscription.remaining_credits = user_subscription.plan.generations_count
                
                user_subscription.save(update_fields=['status', 'end_time', 'remaining_credits'])
                logger.info("Successfully reactivated past_due subscription", extra={'paddle_subscription_id': paddle_subscription_id})
                update_paddle_billing_period_ends_time(paddle_subscription_id, user_subscription.end_time)
            else:
                logger.error("Cannot renew subscription with unexpected status", extra={'paddle_data': data})
    except UserSubscription.DoesNotExist:
        logger.error("Subscription not found for renewal", extra={'paddle_data': data})
    except Exception as e:
        logger.error("Failed to renew subscription", extra={'paddle_data': data, 'error': str(e)}, exc_info=True)

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
        logger.info("Successfully updated Paddle billing period", extra={'paddle_subscription_id': paddle_subscription_id})
    except Exception as e:
        logger.error("Failed to update Paddle billing period", extra={'paddle_subscription_id': paddle_subscription_id, 'error': str(e)}, exc_info=True)

def handle_transaction_past_due(data):
    paddle_subscription_id = data.get('subscription_id')
    
    try:
        with transaction.atomic():
            user_subscription = UserSubscription.objects.select_for_update().get(paddle_subscription_id=paddle_subscription_id)

            if user_subscription.status == UserSubscription.SubscriptionStatus.PAST_DUE:
                logger.error("Subscription already in past_due status, skipping past_due handling", extra={'paddle_data': data})
                return

            user_subscription.status = UserSubscription.SubscriptionStatus.PAST_DUE
            user_subscription.end_time = parse_datetime(data.get('billing_period').get('ends_at'))
            
            user_subscription.save(update_fields=['status', 'end_time'])
            logger.info("Successfully set status to PAST_DUE", extra={'paddle_subscription_id': paddle_subscription_id})
    except UserSubscription.DoesNotExist:
        logger.error("Subscription not found for past_due handling", extra={'paddle_data': data})
    except Exception as e:
        logger.error("Failed to handle past_due event", extra={'paddle_data': data, 'error': str(e)}, exc_info=True)
    
def handle_subscription_updated(data):
    paddle_subscription_id = data.get('id')
    status = data.get('status')
    scheduled_change = data.get('scheduled_change')

    try:
        with transaction.atomic():
            user_subscription = UserSubscription.objects.select_for_update().get(paddle_subscription_id=paddle_subscription_id)

            if status == 'active' and not scheduled_change:
                if user_subscription.cancels_at is not None:
                    user_subscription.cancels_at = None
                    user_subscription.save(update_fields=['cancels_at'])
                    logger.info("Successfully reactivated subscription by removing cancels_at", extra={'paddle_subscription_id': paddle_subscription_id})
                    return
                else:
                    logger.info("Skipping update for active subscription", extra={'paddle_subscription_id': paddle_subscription_id})
                    return
            elif status == 'active' and scheduled_change and scheduled_change.get('action') == 'cancel':
                user_subscription.cancels_at = parse_datetime(scheduled_change.get('effective_at'))
                user_subscription.save(update_fields=['cancels_at'])
                logger.info("Successfully scheduled cancellation", extra={'paddle_subscription_id': paddle_subscription_id})
                return
            elif status == 'past_due':
                logger.info("Skipping update, status is past_due (handled by another event)", extra={'paddle_subscription_id': paddle_subscription_id})
                return
            elif status == 'canceled':
                logger.info("Skipping update, status is canceled (handled by another event)", extra={'paddle_subscription_id': paddle_subscription_id})
                return    
            else:
                logger.error("Unhandled subscription updated scenario", extra={'paddle_data': data})
    except UserSubscription.DoesNotExist:
        logger.error("Subscription not found for update handling", extra={'paddle_data': data})
    except Exception as e:
        logger.error("Failed to handle subscription update", extra={'paddle_data': data, 'error': str(e)}, exc_info=True)

def handle_subscription_canceled(data):
    paddle_subscription_id = data.get('id')
    
    try:
        with transaction.atomic():
            user_subscription = UserSubscription.objects.select_related('plan').select_for_update().get(paddle_subscription_id=paddle_subscription_id)

            if user_subscription.status == UserSubscription.SubscriptionStatus.CANCELED:
                logger.error("Subscription already canceled, skipping cancellation", extra={'paddle_data': data})
                return

            user_subscription.status = UserSubscription.SubscriptionStatus.CANCELED
            user_subscription.cancels_at = None
            user_subscription.save(update_fields=['status', 'cancels_at'])

            config = ApplicationConfig.objects.select_for_update().get_solo()
            config.reserved_for_spend = F('reserved_for_spend') - user_subscription.plan.product_price
            config.save(update_fields=['reserved_for_spend'])

            logger.info("Successfully CANCELED subscription", extra={'paddle_subscription_id': paddle_subscription_id})
    except UserSubscription.DoesNotExist:
        logger.error("Subscription not found for cancellation", extra={'paddle_data': data})
    except Exception as e:
        logger.error("Failed to cancel subscription", extra={'paddle_data': data, 'error': str(e)}, exc_info=True)