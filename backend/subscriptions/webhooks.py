from rest_framework.decorators import permission_classes, authentication_classes, api_view
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.conf import settings
from google.cloud import tasks_v2
from google.cloud.tasks_v2.types import HttpMethod
from google.protobuf import duration_pb2
from django.db import DatabaseError
from . import services
import logging
import hmac
import hashlib
import time
import json

logger = logging.getLogger(__name__)
tasks_client = tasks_v2.CloudTasksClient()

@api_view(['POST'])
@authentication_classes([])
@permission_classes([AllowAny])
def wayforpay_handler(request):
    data = json.loads(request.body.decode('utf-8'))
    merchant_secret_key = settings.WAYFORPAY_SECRET_KEY
    received_signature = data.get('merchantSignature')
    string_for_sign = f"{data.get('merchantAccount', '')};{data.get('orderReference', '')};{data.get('amount', '')};{data.get('currency', '')};{data.get('authCode', '')};{data.get('cardPan', '')};{data.get('transactionStatus', '')};{data.get('reasonCode', '')}"
    
    expected_signature = hmac.new(
        merchant_secret_key.encode('utf-8'),
        string_for_sign.encode('utf-8'),
        hashlib.md5
    ).hexdigest()

    if received_signature != expected_signature:
        logger.error("Invalid WayForPay signature", extra={'data': data})
    else:
        try:
            target_url = f"{settings.WEB_WORKER_URL.rstrip('/')}/webhooks/subscriptions/tasks/"

            queue_path = tasks_client.queue_path(
                settings.GCP_PROJECT_ID,
                settings.GCP_TASKS_LOCATION,
                settings.GCP_TASKS_WAYFORPAY_EVENTS_QUEUE_ID
            )

            task = {
                'http_request': {
                    'url': target_url,
                    'http_method': HttpMethod.POST,
                    'headers': {
                        'Content-Type': 'application/json',
                        'X-Task-Secret': settings.GCP_TASKS_SECRET_KEY,
                    },
                    'body': request.body
                },
                'dispatch_deadline': duration_pb2.Duration(seconds=60)
            }

            tasks_client.create_task(request={'parent': queue_path, 'task': task})
        except Exception:
            return Response(status=400)

    order_reference = data.get('orderReference')
    status = 'accept'
    current_time = int(time.time())
    response_string_for_sign = f"{order_reference};{status};{current_time}"
    
    response_signature = hmac.new(
        merchant_secret_key.encode('utf-8'),
        response_string_for_sign.encode('utf-8'),
        hashlib.md5
    ).hexdigest()

    return Response({
        "orderReference": order_reference,
        "status": status,
        "time": current_time,
        "signature": response_signature
    }, status=200)

@api_view(['POST'])
@authentication_classes([])
@permission_classes([AllowAny])
def tasks_handler(request):
    incoming_secret = request.headers.get('X-Task-Secret')
    if not incoming_secret or incoming_secret != settings.GCP_TASKS_SECRET_KEY:
        logger.error("Unauthorized task attempt", extra={'remote_addr': request.META.get('REMOTE_ADDR')})
        return Response(status=401)

    try:
        data = request.data
        status = data.get('transactionStatus').lower()
        
        if status == 'approved':
            services.create_or_renew_subscription(data)
        elif status in ['inprocessing', 'waitingauthcomplete'] or 'antifraud' in status:
            logger.info("Transaction is processing, holding or antifraud check", extra={"order_reference": data.get('orderReference'), "status": status})
        elif status in ['refunded', 'voided', 'refundinprocessing']:
            logger.info("Refund process", extra={"order_reference": data.get('orderReference'), "status": status})
        elif status in ['declined', 'expired']:
            logger.info("Transaction failed", extra={"order_reference": data.get('orderReference'), "status": status})
        else:
            logger.error("Unhandled transaction status", extra={"order_reference": data.get('orderReference'), "status": status})
    except DatabaseError as e:
        logger.error(f"Database error while processing task", extra={'data': data, 'error': str(e)}, exc_info=True)
        raise
    except Exception as e:
        logger.error(f"Failed to process task", extra={'data': data, 'error': str(e)}, exc_info=True)
        
    return Response(status=204)