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

    try:
        package_id = int(payload_str)
        package = StarPackage.objects.get(id=package_id)
    except (ValueError, StarPackage.DoesNotExist):
        logger.error(f"Invalid package ID in payment payload: {payload_str}")
        return

    config = ApplicationConfig.get_solo()
    config.generations_reserved = F('generations_reserved') + package.generations_count
    config.save(update_fields=['generations_reserved'])

    user.profile.credits += package.generations_count
    user.profile.save()

    # Зберігаємо чек
    UserPurchase.objects.create(
        user=user,
        stars_count=amount,
        generations_count=package.generations_count,
        transaction_id=telegram_payment_charge_id
    )