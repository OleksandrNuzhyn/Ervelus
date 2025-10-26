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
    event_data = None

    try:
        event_data = json.loads(request.body.decode('utf-8'))
        task_type = event_data.get('task_type')
        payload = event_data.get('payload', {})

        if task_type == 'generate_image':
            generation_request_id = payload.get('generation_request_id')
            input_image_url = payload.get('input_image_url')
            await services.handle_generation_process(generation_request_id, input_image_url)
        elif task_type == 'update_after_resize':
            generation_request_id = payload.get('generation_request_id')
            update_data = payload.get('update_data')
            await services.handle_update_after_resize(generation_request_id, update_data)
        else:
            logger.error(f"Received unknown task type", extra={'event_data': event_data})
    except Exception as e:
        logger.error(f"An error occurred while handling task", extra={'event_data': event_data, 'error': str(e)}, exc_info=True)

    return Response(status=204)