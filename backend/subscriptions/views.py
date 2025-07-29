import json
from subscriptions import services
from adrf.decorators import api_view
from rest_framework.decorators import permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from .services import create_customer_portal_session

@api_view(['POST'])
@authentication_classes([])
@permission_classes([AllowAny])
async def pubsub_push_handler(request):
    try:
        event = json.loads(request.body)
    except Exception:
        return Response(status=400)

    try:
        event_type = event.get('event_type')

        if event_type == 'subscription.activated':
            await services.handle_subscription_activated(event['data'])
    except Exception:
        return Response(status=500)
    
    return Response(status=204)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
async def customer_portal_session_create(request):
    try:
        portal_url = await create_customer_portal_session(request.user)
        return Response({'portal_url': portal_url}, status=201)
    except Exception:
        return Response(status=500)