from agreements.permissions import HasAcceptedLatestAgreements
from google.cloud.tasks_v2.types import HttpMethod
from .pagination import CustomPaginationClass
from rest_framework.response import Response
from rest_framework.decorators import action
from google.protobuf import duration_pb2
from .models import GenerationRequest
from rest_framework import viewsets
from urllib.parse import urlparse
from google.cloud import tasks_v2
from django.conf import settings
from . import serializers
from . import services
import logging
import json
import os

tasks_client = tasks_v2.CloudTasksClient()
logger = logging.getLogger(__name__)


class GenerationRequestViewSet(viewsets.ViewSet):
    permission_classes = [HasAcceptedLatestAgreements]

    def create(self, request, *args, **kwargs):
        latest_request = GenerationRequest.objects.filter(user=request.user).order_by('-created_at').first()
        if latest_request and latest_request.status == GenerationRequest.GenerationStatus.PROCESSING:
            return Response({"detail": "You already have a generation in progress"}, status=400)

        serializer = serializers.GenerationRequestCreateSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)

        input_image_file = serializer.validated_data['input_image']
        
        try:
            input_image_url = services.upload_input_image_to_gcs(
                image_file=input_image_file,
                user_id=request.user.id,
            )
        except Exception as e:
            logger.error(f"Failed to upload input image to GCS", extra={'user_id': request.user.id, 'error': str(e)}, exc_info=True)
            return Response(status=400)
        
        try:
            generation_request = GenerationRequest.objects.create(
                user=request.user,
                chosen_style=serializer.validated_data['chosen_style']
            )
        except Exception as e:
            logger.error(f"Failed to create generation request", extra={'user_id': request.user.id, 'error': str(e)}, exc_info=True)
            return Response(status=400)

        try:
            target_url = f"{settings.GENERATIONS_WORKER_URL.rstrip('/')}/webhooks/generations/tasks/"
            
            event_data = {
                "task_type": "generate_image",
                "payload": {
                    "generation_request_id": generation_request.id,
                    "input_image_url": input_image_url
                }
            }

            queue_path = tasks_client.queue_path(
                settings.GCP_PROJECT_ID,
                settings.GCP_TASKS_LOCATION,
                settings.GCP_TASKS_GENERATION_EVENTS_QUEUE_ID,
            )

            task = {
                'http_request': {
                    'url': target_url,
                    'http_method': HttpMethod.POST,
                    'headers': {'Content-Type': 'application/json'},
                    'body': json.dumps(event_data).encode('utf-8')
                },
                'dispatch_deadline': duration_pb2.Duration(seconds=40)
            }

            tasks_client.create_task(request={'parent': queue_path, 'task': task})
        except Exception as e:
            logger.error(f"Failed to create task", extra={'generation_request_id': generation_request.id, 'error': str(e)}, exc_info=True)
            return Response(status=400)

        serializer = serializers.GenerationRequestSerializer(generation_request)
        return Response(serializer.data, status=202)

    def list(self, request, *args, **kwargs):
        queryset = (
            GenerationRequest.objects.filter(
                user=request.user,
                status=GenerationRequest.GenerationStatus.COMPLETED
            )
            .order_by('-created_at')
        )
        
        paginator = CustomPaginationClass()
        page = paginator.paginate_queryset(queryset, request, view=self)

        if page is not None:
            serializer = serializers.GenerationRequestListSerializer(page, many=True)
            return paginator.get_paginated_response(serializer.data)

        serializer = serializers.GenerationRequestListSerializer(queryset, many=True)
        return Response(serializer.data, status=200)

    def retrieve(self, request, pk=None, *args, **kwargs):
        try:
            generation_request = GenerationRequest.objects.select_related('chosen_style').get(
                pk=pk, 
                user=request.user,
                status=GenerationRequest.GenerationStatus.COMPLETED
            )
        except GenerationRequest.DoesNotExist:
            return Response({"detail": "Generation not found or is unavailable"}, status=404)

        serializer = serializers.GenerationRequestSerializer(generation_request)
        return Response(serializer.data, status=200)

    def update(self, request, *args, **kwargs):
        return Response(status=405)

    def partial_update(self, request, *args, **kwargs):
        return Response(status=405)
        
    def destroy(self, request, pk=None, *args, **kwargs):
        try:
            generation_request = GenerationRequest.objects.get(pk=pk, user=request.user)
        except GenerationRequest.DoesNotExist:
            return Response(status=404)

        try:
            image_urls = [
                generation_request.input_thumb_url,
                generation_request.input_large_url,
                generation_request.output_thumb_url,
                generation_request.output_large_url,
                generation_request.output_original_url,
            ]
            
            services.schedule_image_deletion(image_urls)
            generation_request.delete()

            return Response(status=204)
        except Exception as e:
            logger.error(f"Failed to delete generation request", extra={'generation_request_id': generation_request.id, 'error': str(e)}, exc_info=True)
            return Response(status=400)

    @action(detail=False, methods=['GET'])
    def latest(self, request, *args, **kwargs):
        latest_user_generation_request = GenerationRequest.objects.select_related('chosen_style').filter(user=request.user).order_by('-created_at').first()

        if not latest_user_generation_request:
            return Response(status=204)
        
        serializer = serializers.GenerationRequestSerializer(latest_user_generation_request, context={'view': self})
        return Response(serializer.data, status=200)
    
    @action(detail=True, methods=['GET'])
    def download(self, request, pk=None, *args, **kwargs):
        try:
            generation_request = GenerationRequest.objects.get(
                pk=pk,
                user=request.user,
                status=GenerationRequest.GenerationStatus.COMPLETED
            )
        except GenerationRequest.DoesNotExist:
            return Response({"detail": "Generation not found or is unavailable"}, status=404)

        if not generation_request.output_original_url:
            return Response({"detail": "Output image is unavailable for this generation"}, status=400)

        try:
            parsed_url = urlparse(generation_request.output_original_url)
            filename = os.path.basename(parsed_url.path)
            
            download_url = services.generate_signed_gcs_url(
                generation_request.output_original_url,
                expires_in_seconds=30,
                response_disposition=f"attachment; filename={filename}"
            )
            
            return Response({"download_url": download_url}, status=200)
        except Exception as e:
            logger.error(f"Failed to generate download URL for output image", extra={'generation_request_id': generation_request.id, 'error': str(e)}, exc_info=True)
            return Response({"detail": "Failed to retrieve download URL"}, status=400)