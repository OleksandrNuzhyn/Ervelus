from core.models import ApplicationConfig
from asgiref.sync import async_to_sync
from users.models import UserProfile
from init_data_py import InitData
from django.db import transaction
from django.conf import settings
from .messages import MESSAGES
from django.db.models import F
import geoip2.database
import geoip2.errors
import telegram
import logging
import os
import re

logger = logging.getLogger(__name__)
bot = telegram.Bot(token=settings.TELEGRAM_API_KEY)

def validate_telegram_init_data(init_data):
    try:
        parsed_data = InitData.parse(init_data)
        
        if not parsed_data.validate(bot_token=settings.TELEGRAM_API_KEY, raise_error=False):
            raise Exception("Invalid init_data")
        
        if not parsed_data.user:
            raise Exception("User data missing")

        return parsed_data.user.to_dict()
    except Exception as e:
        raise Exception(str(e))
    
def get_country_code_from_ip_address(ip_address):
    try:
        db_path = os.path.join(settings.BASE_DIR, 'geoip', 'GeoLite2-Country.mmdb')
        with geoip2.database.Reader(db_path) as reader:
            response = reader.country(ip_address)
            if response.country.iso_code:
                return response.country.iso_code.lower()
    except geoip2.errors.AddressNotFoundError:
        logger.error("IP address not found in GeoLite2 database", extra={"ip_address": ip_address})
    except Exception as e:
        logger.error("Failed to get country from IP", extra={"ip_address": ip_address, "error": str(e), "exc_info": True})
    return None

def send_message_to_user(telegram_id, message_key, language_code, **context):
    language_code_key = language_code[:2] if language_code else 'en'
    country_messages_dict = MESSAGES.get(language_code_key) or {}
    message = country_messages_dict.get(message_key) or MESSAGES.get('en', {}).get(message_key)

    if not message:
        logger.error("Message key not found", extra={"message_key": message_key, "language_code": language_code})
        return

    try:
        text = message.format(**context)
        async_to_sync(bot.send_message)(
            chat_id=telegram_id,
            text=text
        )
    except Exception as e:
        logger.error("Failed to send message to user", extra={"telegram_id": telegram_id, "message_key": message_key, "language_code": language_code, "error": str(e)}, exc_info=True)

@transaction.atomic
def handle_chat_member(update):
    chat_member = update.chat_member
    
    if chat_member.new_chat_member.status == telegram.ChatMember.MEMBER:
        telegram_id = chat_member.from_user.id
        language_code = chat_member.from_user.language_code
        
        try:
            user_profile = UserProfile.objects.get(telegram_id=telegram_id)
            
            if not user_profile.is_subscribed:
                user_profile.credits += 1
                user_profile.is_subscribed = True
                user_profile.save(update_fields=['credits', 'is_subscribed'])
                
                config = ApplicationConfig.get_solo()
                config.reserved_generations = F('reserved_generations') + 1
                config.save(update_fields=['reserved_generations'])

                send_message_to_user(
                    telegram_id=telegram_id,
                    message_key='subscription_bonus',
                    language_code=language_code
                )
        except UserProfile.DoesNotExist:
            pass
        except Exception as e:
            logger.error("Error handling chat member webhook", extra={"error": str(e)}, exc_info=True)

def handle_message_text_start(update):
    message = update.message
    
    send_message_to_user(
        telegram_id=message.from_user.id,
        message_key='start_message',
        language_code=message.from_user.language_code
    )

def handle_message(update):
    message = update.message
    sender_id = str(message.from_user.id)
    admin_id = "790079946"

    if sender_id == admin_id:
        if message.reply_to_message:
            original_text = message.reply_to_message.text or ''
            telegram_id = re.search(r"ID: (\d+)", original_text)
            
            if telegram_id:
                telegram_id = telegram_id.group(1)

                try:
                    async_to_sync(bot.send_message)(
                        chat_id=telegram_id,
                        text=message.text
                    )

                    async_to_sync(bot.send_message)(
                        chat_id=admin_id,
                        text="Reply sent",
                        reply_to_message_id=message.message_id
                    )
                except Exception as e:
                    async_to_sync(bot.send_message)(
                        chat_id=admin_id,
                        text=f"Failed to send reply: {e}",
                        reply_to_message_id=message.message_id
                    )
            else:
                async_to_sync(bot.send_message)(
                    chat_id=admin_id,
                    text="Please reply to the message containing ID",
                    reply_to_message_id=message.message_id
                )
        return
    
    header_text = (
        f"New Message from User\n"
        f"Name: {message.from_user.first_name} {message.from_user.last_name or ''}\n"
        f"Username: @{message.from_user.username or 'N/A'}\n"
        f"ID: {sender_id}\n"
    )

    try:
        async_to_sync(bot.send_message)(
            chat_id=admin_id,
            text=header_text
        )
        
        async_to_sync(bot.forward_message)(
            chat_id=admin_id,
            from_chat_id=sender_id,
            message_id=message.message_id
        )
    except Exception as e:
        logger.error("Failed to forward message to admin", extra={"error": str(e)}, exc_info=True)