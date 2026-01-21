import hmac
import json
import hashlib
from urllib.parse import parse_qsl
from django.conf import settings

def validate_telegram_init_data(init_data):
    try:
        telegram_data = dict(parse_qsl(init_data))
        if "hash" not in telegram_data:
            raise Exception("Hash missing in initData")

        received_hash = telegram_data.pop("hash")
        telegram_data.pop("signature", None)
        
        data_check_string = "\n".join(f"{k}={v}" for k, v in sorted(telegram_data.items()))
        
        # DEBUG LOGGING (REMOVE AFTER FIXING)
        api_key_masked = settings.TELEGRAM_API_KEY[:5] + "***" if settings.TELEGRAM_API_KEY else "NONE"
        print(f"DEBUG: API_KEY={api_key_masked}")
        print(f"DEBUG: Data Check String:\n{data_check_string}")
        print(f"DEBUG: Received Hash: {received_hash}")
        
        secret_key = hmac.new(b"WebAppData", settings.TELEGRAM_API_KEY.encode(), hashlib.sha256).digest()
        calculated_hash = hmac.new(secret_key, data_check_string.encode(), hashlib.sha256).hexdigest()

        print(f"DEBUG: Calculated Hash: {calculated_hash}")

        if calculated_hash != received_hash:
            raise Exception(f"Invalid hash signature. Calculated: {calculated_hash}, Received: {received_hash}")

        return json.loads(telegram_data["user"])
    except Exception as e:
        # Прокидаємо повну помилку для логера
        raise Exception(f"{str(e)}")