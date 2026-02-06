from rest_framework.decorators import permission_classes, authentication_classes, api_view
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from asgiref.sync import async_to_sync
from products.models import StarPackage
from users.models import UserProfile
from django.conf import settings
from . import services
import telegram
import logging
import json

logger = logging.getLogger(__name__)
bot = telegram.Bot(token=settings.TELEGRAM_API_KEY)

@api_view(['POST'])
@authentication_classes([])
@permission_classes([AllowAny])
def telegram_handler(request):
    secret_token = request.headers.get("X-Telegram-Bot-Api-Secret-Token")
    if getattr(settings, 'TELEGRAM_WEBHOOK_SECRET', None) and secret_token != settings.TELEGRAM_WEBHOOK_SECRET:
        return Response(status=403)

    try:
        data = json.loads(request.body)
        update = telegram.Update.de_json(data, bot)

        if update.pre_checkout_query:
            query = update.pre_checkout_query
            payload = query.invoice_payload
            
            is_ok = True
            error_message = ""
            
            try:
                # Basic validation ensuring payload isn't garbage
                # New format: generations|stars
                if "|" in payload:
                    gen, stars = payload.split("|")
                    int(gen)
                    int(stars)
                else:
                    # Legacy: just ID
                    int(payload)
            except Exception:
                is_ok = False
                error_message = "Invalid payload format."
            
            # Answer asynchronously (converted to sync)
            async def answer():
                await query.answer(ok=is_ok, error_message=error_message)
            
            async_to_sync(answer)()
            return Response(status=200)

        # 2. Successful Payment
        if update.message and update.message.successful_payment:
            payment = update.message.successful_payment
            
            # Identify user
            user_id = update.effective_user.id
            payload = payment.invoice_payload
            telegram_charge_id = payment.telegram_payment_charge_id
            amount = payment.total_amount

            try:
                profile = UserProfile.objects.select_related('user').get(telegram_id=str(user_id))
                user = profile.user
                
                # Atomic transaction
                services.process_star_payment(user, telegram_charge_id, amount, payload)
            except UserProfile.DoesNotExist:
                logger.error(f"Payment received from unknown Telegram user: {user_id}")
                # We return 200 because retrying won't help if user is not in DB.
                # Ideally we should refund or alert admin.
            except Exception as e:
                # If DB error or logic error -> return 500 to trigger Telegram retry
                logger.error(f"Error processing payment: {e}", exc_info=True)
                return Response(status=500)
                
            return Response(status=200)

    except Exception as e:
        logger.error(f"Error processing Telegram webhook: {e}", exc_info=True)
        # Return 500 for generic errors so Telegram retries
        return Response(status=500)

    return Response(status=200)