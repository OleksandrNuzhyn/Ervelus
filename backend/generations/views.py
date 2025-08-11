import json
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from .models import GenerationRequest
from . import services
from .serializers import GenerationRequestCreateSerializer, GenerationRequestSerializer
from google.cloud import tasks_v2
from google.cloud.tasks_v2.types import HttpMethod
from google.protobuf import duration_pb2
from django.conf import settings

tasks_client = tasks_v2.CloudTasksClient()


class GenerationRequestViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = GenerationRequestCreateSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)

        input_image_file = serializer.validated_data['input_image']
        
        input_image_url = services.upload_input_image_to_gcs(
            image_file=input_image_file,
            user_id=request.user.id,
        )
        
        generation_request = GenerationRequest.objects.create(
            user=request.user,
            chosen_style=serializer.validated_data['chosen_style'],
            input_img_url=input_image_url,
        )
        
        try:
            queue_path = tasks_client.queue_path(
                settings.GCP_PROJECT_ID,
                settings.GCP_TASKS_LOCATION,
                settings.GCP_TASKS_GENERATION_EVENTS_QUEUE_ID,
            )

            target_url = f"{settings.BACKEND_URL.rstrip('/')}/webhooks/generations/tasks/"
            
            event_data = {
                'generation_request_id': generation_request.id,
                'resolution': serializer.validated_data['resolution']
            }

            task = {
                'http_request': {
                    'url': target_url,
                    'http_method': HttpMethod.POST,
                    'headers': {'Content-Type': 'application/json'},
                    'body': json.dumps(event_data).encode('utf-8')
                },
                'dispatch_deadline': duration_pb2.Duration(seconds=350)
            }

            tasks_client.create_task(request={'parent': queue_path, 'task': task})
        except Exception:
            return Response({"error": "Failed to publish generation task"}, status=500)

        serializer = GenerationRequestSerializer(generation_request)
        return Response(serializer.data, status=202)

    def list(self, request, *args, **kwargs):
        return Response(status=405)

    def retrieve(self, request, *args, **kwargs):
        return Response(status=405)

    def update(self, request, *args, **kwargs):
        return Response(status=405)

    def partial_update(self, request, *args, **kwargs):
        return Response(status=405)
        
    def destroy(self, request, *args, **kwargs):
        return Response(status=405)

    @action(detail=False, methods=['get'])
    def latest(self, request, *args, **kwargs):
        latest_user_generation_request = GenerationRequest.objects.filter(user=request.user).order_by('-created_at').first()

        if not latest_user_generation_request:
            return Response(None, status=200)
        
        serializer = GenerationRequestSerializer(latest_user_generation_request)
        return Response(serializer.data, status=200)
