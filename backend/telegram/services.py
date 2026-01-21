import hmac
import json
import hashlib
from urllib.parse import parse_qsl
from urllib.parse import unquote
from django.conf import settings

def validate_telegram_init_data(init_data):
    # Прибираємо можливі пробіли/лапки з токена
    bot_token = settings.TELEGRAM_API_KEY.strip().strip('"').strip("'")
    
    try:
        # 1. Розбиваємо рядок за допомогою unquote вручну, щоб не було сюрпризів з '+' або іншими символами
        params = {}
        for item in init_data.split('&'):
            if '=' in item:
                k, v = item.split('=', 1)
                params[k] = unquote(v)
        
        if "hash" not in params:
            raise Exception("Hash missing in initData")

        received_hash = params.pop("hash")
        params.pop("signature", None) # Видаляємо signature, якщо є
        
        # 2. Сортуємо ключі за алфавітом
        sorted_keys = sorted(params.keys())
        data_check_string = "\n".join(f"{k}={params[k]}" for k in sorted_keys)
        
        # DEBUG LOGGING
        print(f"DEBUG: Token Length: {len(bot_token)}")
        print(f"DEBUG: Data Check String:\n{data_check_string}")
        
        # 3. Рахуємо секретний ключ
        secret_key = hmac.new(b"WebAppData", bot_token.encode(), hashlib.sha256).digest()
        
        # 4. Рахуємо хеш
        calculated_hash = hmac.new(secret_key, data_check_string.encode(), hashlib.sha256).hexdigest()

        if calculated_hash != received_hash:
            raise Exception(f"Hash mismatch. Calc: {calculated_hash[:10]}... Rec: {received_hash[:10]}...")

        return json.loads(params["user"])
    except Exception as e:
        raise Exception(str(e))