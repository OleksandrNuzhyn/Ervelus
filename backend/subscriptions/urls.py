from django.urls import path
from . import webhooks


urlpatterns = [
    path('paddle/', webhooks.paddle_webhook_handler, name='paddle-webhook'),
]