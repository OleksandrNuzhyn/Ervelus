from init_data_py import InitData
from django.conf import settings
import requests
import logging

logger = logging.getLogger(__name__)

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
        response = requests.get(f'https://ipapi.co/{ip_address}/country/', timeout=1)
        if response.status_code == 200:
            return response.text.strip().lower()
    except Exception as e:
        logger.error("Failed to get country from IP", extra={"ip": ip, "error": str(e), "exc_info": True})
    return None