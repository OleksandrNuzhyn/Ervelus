from generations.services import generate_signed_gcs_url
from generations.models import GenerationRequest
from asgiref.sync import async_to_sync
from users.models import UserProfile
from urllib.parse import parse_qsl
from django.db import transaction
from django.conf import settings
from .messages import MESSAGES
import geoip2.database
import geoip2.errors
import telegram
import logging
import hashlib
import hmac
import json
import os
import re

logger = logging.getLogger(__name__)
bot = telegram.Bot(token=settings.TELEGRAM_API_KEY)

def validate_telegram_init_data(init_data):
    try:
        parsed_data = dict(parse_qsl(init_data))
        received_hash = parsed_data.pop("hash", None)

        if not received_hash:
            raise Exception("Hash is missing")
        
        data_check_string = "\n".join(
            f"{k}={v}" for k, v in sorted(parsed_data.items())
        )
        
        secret_key = hmac.new(
            b"WebAppData", 
            settings.TELEGRAM_API_KEY.encode("utf-8"), 
            hashlib.sha256
        ).digest()
        
        calculated_hash = hmac.new(
            secret_key, 
            data_check_string.encode("utf-8"), 
            hashlib.sha256
        ).hexdigest()
        
        if not hmac.compare_digest(calculated_hash, received_hash):
            raise Exception("Invalid init_data")
            
        parsed_user_data = parsed_data.get("user")
        if not parsed_user_data:
            raise Exception("User data missing")
            
        return json.loads(parsed_user_data)
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
                user_profile.free_credits += 1
                user_profile.is_subscribed = True
                user_profile.save(update_fields=['free_credits', 'is_subscribed'])

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

def handle_inline_query(update):
    query = update.inline_query.query
    telegram_id = str(update.effective_user.id)
    results = []

    if query == 'invite':
        results.append(
            telegram.InlineQueryResultArticle(
                id=query,
                title="Invite to Ervelus",
                description="Share an invite link with your friends",
                input_message_content=telegram.InputTextMessageContent(
                    "https://t.me/ervelus_bot/app"
                )
            )
        )
    elif query.isdigit():
        try:
            generation_request = GenerationRequest.objects.get(id=query, user__profile__telegram_id=telegram_id)
            
            if generation_request.output_original_url and generation_request.output_thumb_url:
                try:
                    signed_original_url = generate_signed_gcs_url(generation_request.output_original_url, 300)
                    signed_thumb_url = generate_signed_gcs_url(generation_request.output_thumb_url, 300)
                except Exception as e:
                    logger.error("Failed to sign URLs for inline query", extra={'error': str(e)}, exc_info=True)
                    return

                results.append(
                    telegram.InlineQueryResultPhoto(
                        id=query,
                        photo_url=signed_original_url,
                        thumbnail_url=signed_thumb_url,
                        title="Share Generation",
                        description="Tap to send image",
                        reply_markup=telegram.InlineKeyboardMarkup([[
                            telegram.InlineKeyboardButton("Try it yourself 🎨", url="https://t.me/ervelus_bot/app")
                        ]])
                    )
                )
        except GenerationRequest.DoesNotExist:
            pass
        except Exception as e:
            logger.error("Error while handling generation inline query", extra={"error": str(e)}, exc_info=True)

    try:
        if results:
            async_to_sync(bot.answer_inline_query)(
                inline_query_id=update.inline_query.id,
                results=results,
                cache_time=0
            )
    except Exception as e:
        logger.error("Error while answering the inline query", extra={"error": str(e)}, exc_info=True)