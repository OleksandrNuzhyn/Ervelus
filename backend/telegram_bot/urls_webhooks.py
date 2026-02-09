from django.urls import path
from . import webhooks


urlpatterns = [
    path('', webhooks.telegram_handler, name='telegram-handler'),
]