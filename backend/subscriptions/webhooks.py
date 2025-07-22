from django.conf import settings
from django.http import HttpRequest, HttpResponse
from django.views.decorators.csrf import csrf_exempt
# from google.cloud import pubsub_v1
from paddle_billing.Notifications import Secret, Verifier

@csrf_exempt
async def paddle_webhook_handler(request: HttpRequest) -> HttpResponse:
    if request.method != 'POST':
        return HttpResponse(status=405)

    try:
        Verifier().verify(request, Secret(settings.PADDLE_WEBHOOK_SECRET_KEY))
    except Exception:
        return HttpResponse(status=400)

    # try:
    #     publisher = pubsub_v1.PublisherClient()
    #     topic_path = publisher.topic_path(settings.GCP_PROJECT_ID, settings.GCP_PUBSUB_PADDLE_TOPIC_ID)
        
    #     future = publisher.publish(topic_path, request.body)
        
    # except Exception:
    #     return HttpResponse(status=500)

    return HttpResponse(status=200)