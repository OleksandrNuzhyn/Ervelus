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
import logging

logger = logging.getLogger(__name__)
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
        target_url = f"{settings.BACKEND_URL.rstrip('/')}/webhooks/subscriptions/tasks/"

        queue_path = tasks_client.queue_path(
            settings.GCP_PROJECT_ID,
            settings.GCP_TASKS_LOCATION,
            settings.GCP_TASKS_PADDLE_EVENTS_QUEUE_ID,
        )

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
        return Response(status=400)

    return Response(status=200)

@api_view(['POST'])
@authentication_classes([])
@permission_classes([AllowAny])
def tasks_handler(request):
    event = None
    event_type = None
    paddle_subscription_id = None
    
    try:
        event = json.loads(request.body.decode('utf-8'))
        event_type = event.get('event_type')

        if event_type == 'transaction.completed':
            services.handle_transaction_completed(event['data'])
        elif event_type == 'transaction.past_due':
            services.handle_transaction_past_due(event['data'])
        elif event_type == 'subscription.updated':
            services.handle_subscription_updated(event['data'])
        elif event_type == 'subscription.canceled':
            services.handle_subscription_canceled(event['data'])
        else:
            logger.error(f"Unhandled event type", extra={'event_type': event_type})
    except Exception as e:
        try:
            if isinstance(event, dict):
                event_type = event.get('event_type')
                data = event.get('data') if isinstance(event.get('data'), dict) else {}

                if event_type in ['transaction.completed', 'transaction.past_due']:
                    paddle_subscription_id = data.get('subscription_id')
                elif event_type in ['subscription.updated', 'subscription.canceled']:
                    paddle_subscription_id = data.get('id')
        except Exception as exc:
            logger.error("Error while extracting paddle_subscription_id in exception handler", extra={'error': str(exc)}, exc_info=True)
        logger.error(f"Failed to process paddle event", extra={'event_type': event_type, 'paddle_subscription_id': paddle_subscription_id, 'error': str(e)}, exc_info=True)
    return Response(status=204)