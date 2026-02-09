from core.models import ApplicationConfig
from asgiref.sync import async_to_sync
from users.models import UserProfile
from .models import UserPurchase
from django.db.models import F
from django.db import transaction
import logging

logger = logging.getLogger(__name__)

@transaction.atomic
def handle_user_purchase(user, payload, transaction_id):
    if UserPurchase.objects.filter(transaction_id=transaction_id).exists():
        logger.error("Duplicate payment webhook received", extra={"transaction_id": transaction_id})
        return

    try:
        generations_count, stars_count = payload.split("|")
        generations_count = int(generations_count)
        stars_count = int(stars_count)
    except Exception as e:
        logger.error("Invalid payload format", extra={"payload": payload, "error": str(e)})
        return

    config = ApplicationConfig.get_solo()
    config.generations_reserved = F('generations_reserved') + generations_count
    config.save(update_fields=['generations_reserved'])

    user.profile.credits += generations_count
    user.profile.save(update_fields=['credits'])

    UserPurchase.objects.create(
        user=user,
        stars_count=stars_count,
        generations_count=generations_count,
        country_code=user.profile.country_code,
        transaction_id=transaction_id
    )

def handle_pre_checkout_query(update):
    query = update.pre_checkout_query
    
    async def answer():
        await query.answer(ok=True)
    
    async_to_sync(answer)()

def handle_message_successful_payment(update):
    payment = update.message.successful_payment
    telegram_id = update.effective_user.id
    payload = payment.invoice_payload
    transaction_id = payment.telegram_payment_charge_id

    try:
        user_profile = UserProfile.objects.select_related('user').get(telegram_id=telegram_id)
        user = user_profile.user
        handle_user_purchase(user, payload, transaction_id)
    except UserProfile.DoesNotExist:
        logger.error("Payment received from unknown user", extra={"telegram_id": telegram_id, "transaction_id": transaction_id})
    except Exception:
        raise