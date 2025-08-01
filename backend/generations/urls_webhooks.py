from django.urls import path
from . import webhooks


urlpatterns = [
    path('pubsub/push/', webhooks.pubsub_push_handler, name='pubsub-push-handler'),
] 