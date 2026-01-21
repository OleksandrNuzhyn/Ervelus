import hmac
import json
import hashlib
from urllib.parse import parse_qsl
from django.conf import settings

def validate_telegram_init_data(init_data):
    try:
        telegram_data = dict(parse_qsl(init_data, keep_blank_values=True))
        received_hash = telegram_data.pop("hash")
        telegram_data.pop("signature", None)
        
        data_check_string = "\n".join(f"{k}={v}" for k, v in sorted(telegram_data.items()))
        
        secret_key = hmac.new(b"WebAppData", settings.TELEGRAM_API_KEY.encode(), hashlib.sha256).digest()
        calculated_hash = hmac.new(secret_key, data_check_string.encode(), hashlib.sha256).hexdigest()

        if calculated_hash != received_hash:
            raise Exception("invalid hash signature")

        return json.loads(telegram_data["user"])
    except Exception as e:
        raise Exception(str(e))