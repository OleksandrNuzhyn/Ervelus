from django.conf import settings
from paddle_billing import Client
import asyncio

paddle_client = Client(settings.PADDLE_API_KEY)

async def handle_subscription_activated(data: dict):
    customer_id = data.get('customer_id')
    subscription_id = data.get('id')
    print(f"--- Обробка 'subscription.activated' ---")
    print(f"  ID клієнта (Paddle): {customer_id}")
    print(f"  ID підписки (Paddle): {subscription_id}")
    print(f"  Повні дані: {data}")
    await asyncio.sleep(1)