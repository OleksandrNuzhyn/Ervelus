from django.conf import settings
from rest_framework.decorators import permission_classes, authentication_classes, api_view
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from google.cloud import pubsub_v1
from paddle_billing.Notifications import Secret, Verifier
from . import services
import json

publisher = pubsub_v1.PublisherClient()

@api_view(['POST'])
@authentication_classes([])
@permission_classes([AllowAny])
def paddle_webhook_handler(request):
    try:
        Verifier().verify(request, Secret(settings.PADDLE_WEBHOOK_SECRET_KEY))
    except Exception:
        return Response(status=400)

    try:
        topic_path = publisher.topic_path(settings.GCP_PROJECT_ID, settings.GCP_PUBSUB_PADDLE_EVENTS_TOPIC_ID)
        future = publisher.publish(topic_path, request.body)
        future.result()
    except Exception:
        return Response(status=500)

    return Response(status=200)

@api_view(['POST'])
@authentication_classes([])
@permission_classes([AllowAny])
def pubsub_push_handler(request):
    try:
        event = json.loads(request.body.decode('utf-8'))
    except Exception:
        return Response(status=400)

    try:
        event_type = event.get('event_type')

        if event_type == 'subscription.activated':
            services.handle_subscription_activated(event['data'])
    except Exception:
        return Response(status=500)
    
    return Response(status=204)