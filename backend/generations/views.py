import json
import logging
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from .models import GenerationRequest
from . import services
from .serializers import (
    GenerationRequestCreateSerializer,
    GenerationRequestListSerializer,
    GenerationRequestSerializer
)
from .pagination import CustomPaginationClass
from google.cloud import tasks_v2
from google.cloud.tasks_v2.types import HttpMethod
from google.protobuf import duration_pb2
from django.conf import settings

tasks_client = tasks_v2.CloudTasksClient()
logger = logging.getLogger(__name__)


class GenerationRequestViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = GenerationRequestCreateSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)

        latest_request = GenerationRequest.objects.filter(user=request.user).order_by('-created_at').first()
        if latest_request and latest_request.status == GenerationRequest.GenerationStatus.PROCESSING:
            return Response({"detail": "You already have a generation in progress. Please wait for it to complete"}, status=400)

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

        serializer = GenerationRequestSerializer(generation_request)
        return Response(serializer.data, status=202)

    def list(self, request, *args, **kwargs):
        queryset = (
            GenerationRequest.objects.filter(
                user=request.user,
                status__in=[GenerationRequest.GenerationStatus.PROCESSING, GenerationRequest.GenerationStatus.COMPLETED],
                is_hidden=False
            ).order_by('-created_at')
        )

        existing_blobs = services.get_user_gcs_blob_names(request.user.id)
        
        paginator = CustomPaginationClass()
        page = paginator.paginate_queryset(queryset, request, view=self)
        serializer = GenerationRequestListSerializer(page, many=True, context={'existing_blobs': existing_blobs})
        
        return paginator.get_paginated_response(serializer.data)

    def retrieve(self, request, pk=None):
        try:
            generation_request = GenerationRequest.objects.get(pk=pk, user=request.user)
        except GenerationRequest.DoesNotExist:
            return Response(status=404)

        if generation_request.is_hidden:
            return Response({"detail": "This generation is currently unavailable"}, status=404)

        serializer = GenerationRequestSerializer(generation_request)
        return Response(serializer.data, status=200)

    def update(self, request, *args, **kwargs):
        return Response(status=405)

    def partial_update(self, request, *args, **kwargs):
        return Response(status=405)
        
    def destroy(self, request, pk=None):
        try:
            generation_request = GenerationRequest.objects.get(pk=pk, user=request.user)
        except GenerationRequest.DoesNotExist:
            return Response(status=404)

        if generation_request.status == GenerationRequest.GenerationStatus.PROCESSING:
            return Response({"detail": "You cannot delete a generation that is currently processing"}, status=400)

        generation_request_id = generation_request.id
        user_id = request.user.id

        try:
            services.delete_generation_request_images_from_gcs(generation_request)
            logger.info(f"Successfully deleted GCS images for generation_request_id='{generation_request_id}', user_id='{user_id}'")
            
            generation_request.delete()
            logger.info(f"Successfully deleted generation_request record. generation_request_id='{generation_request_id}', user_id='{user_id}'")
            
            return Response(status=204)
        except Exception as e:
            logger.error(f"Failed to delete generation_request. generation_request_id='{generation_request_id}', user_id='{user_id}', error='{e}'", exc_info=True)
            return Response(status=500)

    @action(detail=False, methods=['get'])
    def latest(self, request, *args, **kwargs):
        latest_user_generation_request = GenerationRequest.objects.filter(user=request.user).order_by('-created_at').first()

        if not latest_user_generation_request:
            return Response(None, status=204)
        
        if latest_user_generation_request.is_hidden:
            return Response({"detail": "This generation is currently unavailable"}, status=404)
        
        serializer = GenerationRequestSerializer(latest_user_generation_request)
        return Response(serializer.data, status=200)