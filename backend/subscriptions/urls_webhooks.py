from django.urls import path
from . import views, webhooks


urlpatterns = [
    path('paddle/', webhooks.paddle_webhook_handler, name='paddle-webhook-handler'),
    
    path('pubsub/push/', views.pubsub_push_handler, name='pubsub-push-handler'),
] 