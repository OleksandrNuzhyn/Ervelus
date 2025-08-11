from django.urls import path
from . import webhooks


urlpatterns = [
    path('paddle/', webhooks.paddle_handler, name='paddle-handler')
]