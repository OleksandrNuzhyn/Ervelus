import json
from django.http import HttpRequest, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from subscriptions import services

@csrf_exempt
async def pubsub_push_handler(request: HttpRequest) -> HttpResponse:
    if request.method != 'POST':
        return HttpResponse(status=405)

    try:
        event = json.loads(request.body)
    except json.JSONDecodeError:
        return HttpResponse(status=400)

    try:
        event_type = event.get('event_type')

        if event_type == 'subscription.activated':
            await services.handle_subscription_activated(event['data'])
    except Exception:
        return HttpResponse(status=500)
    
    return HttpResponse(status=204)