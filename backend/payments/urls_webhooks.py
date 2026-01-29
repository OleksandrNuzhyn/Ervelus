from django.urls import path
from . import webhooks


urlpatterns = [
    path('telegram/', webhooks.telegram_handler, name='telegram-handler'),
]