from asgiref.sync import async_to_sync
from init_data_py import InitData
from django.conf import settings
from .messages import MESSAGES
import geoip2.database
import geoip2.errors
import telegram
import logging
import os

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

def send_message_to_user(telegram_id, country_code, message_key, **context):
    country_code_key = country_code if country_code else 'en'
    country_messages_dict = MESSAGES.get(country_code_key) or {}
    message = country_messages_dict.get(message_key) or MESSAGES.get('en', {}).get(message_key)

    if not message:
        logger.error("Message key not found", extra={"message_key": message_key, "country_code_key": country_code_key})
        return

    try:
        text = message.format(**context)
        async_to_sync(bot.send_message)(
            chat_id=telegram_id,
            text=text
        )
    except Exception as e:
        logger.error("Failed to send message to user", extra={"telegram_id": telegram_id, "country_code": country_code, "message_key": message_key, "error": str(e)}, exc_info=True)