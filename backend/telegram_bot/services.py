from init_data_py import InitData
from django.conf import settings
import geoip2.database
import geoip2.errors
import logging
import os

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