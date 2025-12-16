from datetime import datetime, timezone
from dateutil.relativedelta import relativedelta
from django.conf import settings
from django.contrib.auth import get_user_model
from .models import UserSubscription
from products.models import SubscriptionPlan
import logging
import requests

User = get_user_model()
logger = logging.getLogger(__name__)

def create_or_renew_subscription(data):
    order_reference = data.get('orderReference')
    rec_token = data.get('recToken')

    order_parts = order_reference.split('_')
    user_id = int(order_parts[0])
    plan_id = int(order_parts[1])

    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        logger.error("User not found for subscription activation", extra={"order_reference": order_reference})
        return

    try:
        subscription = UserSubscription.objects.get(order_reference=order_reference)
    except UserSubscription.DoesNotExist:
        subscription = None
    
    now = datetime.now(timezone.utc)
    end_time_timestamp = get_subscription_end_time(order_reference, subscription)
    
    if end_time_timestamp:
        end_time = datetime.fromtimestamp(end_time_timestamp, tz=timezone.utc)
    else:
        if subscription and subscription.end_time:
            base_date = subscription.end_time
        else:
            base_date = now

        end_time = base_date + relativedelta(months=1)
        logger.error("Could not fetch end time from API, using calculated value", extra={"order_reference": order_reference})
    
    if subscription:
        plan = subscription.plan
        subscription.end_time = end_time
        subscription.rec_token = rec_token
        subscription.remaining_credits = plan.generations_count
        subscription.save()
    else:
        try:
            plan = SubscriptionPlan.objects.get(id=plan_id)
        except SubscriptionPlan.DoesNotExist:
            logger.error("Plan not found", extra={"plan_id": plan_id, "order_reference": order_reference})
            return

        if not plan.is_active:
            logger.error("Subscription creation for inactive plan", extra={"plan_id": plan_id, "order_reference": order_reference})
        
        UserSubscription.objects.create(
            user=user,
            plan=plan,
            start_time=now,
            end_time=end_time,
            is_auto_renew=True,
            rec_token=rec_token,
            order_reference=order_reference,
            remaining_credits=plan.generations_count
        )

def get_subscription_end_time(order_reference, subscription):
    try:
        url = "https://api.wayforpay.com/regularApi"
        payload = {
            "requestType": "STATUS",
            "merchantAccount": settings.WAYFORPAY_MERCHANT_ACCOUNT,
            "merchantPassword": settings.WAYFORPAY_MERCHANT_PASSWORD,
            "orderReference": order_reference
        }
        
        response = requests.post(url, json=payload, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        if data.get('reasonCode') == 4100:
            return data.get('nextPaymentDate')
        
        subscription_id = subscription.id if subscription else None
        logger.error("Failed to fetch nextPaymentDate", extra={"reason": data.get('reason'), "subscription_id": subscription_id})
        return None
    except requests.RequestException as e:
        subscription_id = subscription.id if subscription else None
        logger.error("Network error while fetching subscription nextPaymentDate", extra={"subscription_id": subscription_id, "error": str(e)})
        return None
    except Exception as e:
        subscription_id = subscription.id if subscription else None
        logger.error("Error occurred while fetching subscription nextPaymentDate", extra={"subscription_id": subscription_id, "error": str(e)})
        return None

def cancel_subscription(subscription):
    if not subscription.is_auto_renew:
        logger.error(f"Subscription is already cancelled", extra={"subscription_id": subscription.id})
        return True

    try:
        url = "https://api.wayforpay.com/regularApi"
        payload = {
            "requestType": "REMOVE",
            "merchantAccount": settings.WAYFORPAY_MERCHANT_ACCOUNT,
            "merchantPassword": settings.WAYFORPAY_MERCHANT_PASSWORD,
            "orderReference": subscription.order_reference
        }
        
        response = requests.post(url, json=payload, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        if data.get('reasonCode') == 4100:
            subscription.is_auto_renew = False
            subscription.save()
            return True
        
        logger.error("Failed to cancel subscription", extra={"subscription_id": subscription.id, "reason": data.get('reason')})
        return False
    except requests.RequestException as e:
        logger.error("Network error while cancelling subscription", extra={"subscription_id": subscription.id, "error": str(e)})
        return False
    except Exception as e:
        logger.error("Error occurred while cancelling subscription", extra={"subscription_id": subscription.id, "error": str(e)})
        return False