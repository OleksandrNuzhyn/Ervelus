import json
import logging
from adrf.decorators import api_view
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from . import services

logger = logging.getLogger(__name__)

@api_view(['POST'])
@authentication_classes([])
@permission_classes([AllowAny])
async def tasks_handler(request):
    generation_request_id = None

    try:
        event_data = json.loads(request.body.decode('utf-8'))
        generation_request_id = event_data.get('generation_request_id')
    except Exception as e:
        logger.error(f"Failed to parse generation event data", extra={'error': str(e)}, exc_info=True)

    try:
        await services.handle_generation_process(generation_request_id)
    except Exception as e:
        logger.error(f"Failed to handle generation process", extra={'generation_request_id': generation_request_id, 'error': str(e)}, exc_info=True)

    return Response(status=204)