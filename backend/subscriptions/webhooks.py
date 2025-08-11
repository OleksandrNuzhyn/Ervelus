from django.conf import settings
from rest_framework.decorators import permission_classes, authentication_classes, api_view
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from paddle_billing.Notifications import Secret, Verifier
from google.cloud import tasks_v2
from google.cloud.tasks_v2.types import HttpMethod
from google.protobuf import duration_pb2
from . import services
import json

tasks_client = tasks_v2.CloudTasksClient()

@api_view(['POST'])
@authentication_classes([])
@permission_classes([AllowAny])
def paddle_handler(request):
    try:
        Verifier().verify(request, Secret(settings.PADDLE_WEBHOOK_SECRET_KEY))
    except Exception:
        return Response(status=400)

    try:
        queue_path = tasks_client.queue_path(
            settings.GCP_PROJECT_ID,
            settings.GCP_TASKS_LOCATION,
            settings.GCP_TASKS_PADDLE_EVENTS_QUEUE_ID,
        )

        target_url = f"{settings.BACKEND_URL.rstrip('/')}/webhooks/subscriptions/tasks/"

        task = {
            'http_request': {
                'url': target_url,
                'http_method': HttpMethod.POST,
                'headers': {'Content-Type': 'application/json'},
                'body': request.body
            },
            'dispatch_deadline': duration_pb2.Duration(seconds=60)
        }

        tasks_client.create_task(request={'parent': queue_path, 'task': task})
    except Exception:
        return Response(status=500)

    return Response(status=200)

@api_view(['POST'])
@authentication_classes([])
@permission_classes([AllowAny])
def tasks_handler(request):
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