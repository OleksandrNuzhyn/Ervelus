from init_data_py import InitData
from django.conf import settings

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