from django.conf import settings
from paddle_billing import Client

paddle_client = Client(settings.PADDLE_API_KEY)