import hmac
import json
import hashlib
from urllib.parse import parse_qsl
from django.conf import settings

def validate_telegram_init_data(init_data):
    # 1. Очистка токена
    token = settings.TELEGRAM_API_KEY
    if token:
        token = token.strip().strip("'").strip('"')
    
    try:
        telegram_data = dict(parse_qsl(init_data, keep_blank_values=True))
        
        if "hash" not in telegram_data:
            raise Exception("Hash missing in initData")

        received_hash = telegram_data.pop("hash")
        telegram_data.pop("signature", None)

        # Зберігаємо "сирий" user для першої спроби
        original_user = telegram_data.get('user', '')
        
        # Helper для перевірки
        def check_hash(t_data):
            check_string = "\n".join(f"{k}={v}" for k, v in sorted(t_data.items()))
            secret_key = hmac.new(b"WebAppData", token.encode(), hashlib.sha256).digest()
            calc_hash = hmac.new(secret_key, check_string.encode(), hashlib.sha256).hexdigest()
            return calc_hash == received_hash

        # Спроба 1: Як прийшло (з \/)
        # Якщо Телеграм підписав екранований рядок
        if check_hash(telegram_data):
            return json.loads(original_user)

        # Спроба 2: Виправляємо слеші (\/ -> /)
        # Якщо Телеграм підписав НЕ екранований рядок (стандарт)
        if 'user' in telegram_data:
            telegram_data['user'] = original_user.replace('\\/', '/')
            if check_hash(telegram_data):
                return json.loads(telegram_data['user'])

        raise Exception("Hash mismatch (tried both escaped and unescaped variants)")

    except Exception as e:
        raise Exception(str(e))