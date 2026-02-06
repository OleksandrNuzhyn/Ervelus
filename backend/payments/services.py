from core.models import ApplicationConfig
from products.models import StarPackage
from .models import UserPurchase
from django.db.models import F
from django.db import transaction
import logging

logger = logging.getLogger(__name__)

@transaction.atomic
def process_star_payment(user, telegram_payment_charge_id, amount, payload_str):
    if UserPurchase.objects.filter(transaction_id=telegram_payment_charge_id).exists():
        logger.warning(f"Duplicate payment received: {telegram_payment_charge_id}")
        return

    generations_count = 0
    stars_count = amount  # Default to what Telegram charged
    
    try:
        if "|" in payload_str:
            # New format: generations|stars
            generations_str, stars_str = payload_str.split("|")
            generations_count = int(generations_str)
            # We can use stars from payload or from telegram amount. 
            # Ideally they closely match, but telegram amount is the REAL money paid.
            # Using payload for record keeping if needed, but 'amount' argument is safer for 'UserPurchase.stars_count'.
        else:
            # Legacy format: package_id
            package_id = int(payload_str)
            package = StarPackage.objects.get(id=package_id)
            generations_count = package.generations_count

    except (ValueError, StarPackage.DoesNotExist):
        logger.error(f"Invalid payload or missing package: {payload_str}")
        return

    config = ApplicationConfig.get_solo()
    config.generations_reserved = F('generations_reserved') + generations_count
    config.save(update_fields=['generations_reserved'])

    user.profile.credits += generations_count
    user.profile.save()

    # Зберігаємо чек
    UserPurchase.objects.create(
        user=user,
        stars_count=stars_count,
        generations_count=generations_count,
        transaction_id=telegram_payment_charge_id
    )