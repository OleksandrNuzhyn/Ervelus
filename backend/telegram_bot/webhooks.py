from rest_framework.decorators import permission_classes, authentication_classes, api_view
from payments.services import handle_pre_checkout_query, handle_message_successful_payment
from telegram_bot.services import handle_chat_member
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.conf import settings
import telegram
import logging
import json

logger = logging.getLogger(__name__)
bot = telegram.Bot(token=settings.TELEGRAM_API_KEY)

@api_view(['POST'])
@authentication_classes([])
@permission_classes([AllowAny])
def telegram_handler(request):
    webhook_secret = request.headers.get("X-Telegram-Bot-Api-Secret-Token")
    if webhook_secret != settings.TELEGRAM_WEBHOOK_SECRET:
        return Response(status=403)

    try:
        data = json.loads(request.body)
        update = telegram.Update.de_json(data, bot)

        if update.pre_checkout_query:
            handle_pre_checkout_query(update)
        elif update.message and update.message.successful_payment:
            handle_message_successful_payment(update)
        elif update.chat_member:
            handle_chat_member(update)
    except Exception as e:
        logger.error("Error while handling Telegram webhook", extra={"error": str(e)}, exc_info=True)
        return Response(status=500)

    return Response(status=200)