from rest_framework.permissions import AllowAny
from rest_framework.decorators import authentication_classes, permission_classes
from adrf.decorators import api_view
from rest_framework.response import Response
import json
from . import services

@api_view(['POST'])
@authentication_classes([])
@permission_classes([AllowAny])
async def pubsub_push_handler(request):
    try:
        event_data = json.loads(request.body.decode('utf-8'))
        generation_request_id = event_data.get('generation_request_id')
        resolution = event_data.get('resolution')
    except Exception:
        return Response(status=400)

    try:
        await services.process_generation_from_event(generation_request_id, resolution)
    except Exception:
        return Response(status=500)

    return Response(status=204)