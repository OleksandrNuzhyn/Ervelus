import json
import logging
from . import services
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from agreements.permissions import HasAcceptedLatestAgreements
from .models import GenerationRequest
from .serializers import GenerationRequestCreateSerializer, GenerationRequestListSerializer, GenerationRequestSerializer
from .pagination import CustomPaginationClass
from google.cloud import tasks_v2
from google.cloud.tasks_v2.types import HttpMethod
from google.protobuf import duration_pb2
from django.conf import settings

tasks_client = tasks_v2.CloudTasksClient()
logger = logging.getLogger(__name__)


class GenerationRequestViewSet(viewsets.ViewSet):
    permission_classes = [HasAcceptedLatestAgreements]

    def create(self, request, *args, **kwargs):
        serializer = GenerationRequestCreateSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)

        latest_request = GenerationRequest.objects.filter(user=request.user).order_by('-created_at').first()
        if latest_request and latest_request.status == GenerationRequest.GenerationStatus.PROCESSING:
            return Response({"detail": "You already have a generation in progress. Please wait for it to complete or stop it"}, status=400)

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
                chosen_style=serializer.validated_data['chosen_style'],
                input_img_url=input_image_url,
            )
        except Exception as e:
            logger.error(f"Failed to create generation request", extra={'user_id': request.user.id, 'error': str(e)}, exc_info=True)
            return Response(status=400)

        try:
            target_url = f"{settings.BACKEND_URL.rstrip('/')}/webhooks/generations/tasks/"
            
            event_data = {
                'generation_request_id': generation_request.id,
                'resolution': serializer.validated_data['resolution']
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
                'dispatch_deadline': duration_pb2.Duration(seconds=350)
            }

            tasks_client.create_task(request={'parent': queue_path, 'task': task})
        except Exception as e:
            logger.error(f"Failed to create task", extra={'generation_request_id': generation_request.id, 'error': str(e)}, exc_info=True)
            return Response(status=400)

        serializer = GenerationRequestSerializer(generation_request)
        return Response(serializer.data, status=202)

    def list(self, request, *args, **kwargs):
        queryset = (
            GenerationRequest.objects.filter(
                user=request.user,
                is_hidden=False
            ).order_by('-created_at')
        )

        existing_blobs_names = []
        try:
            existing_blobs_names = services.get_user_gcs_all_blob_names(request.user.id)
        except Exception as e:
            logger.error(f"Failed to get user GCS blob names", extra={'user_id': request.user.id, 'error': str(e)}, exc_info=True)
        
        paginator = CustomPaginationClass()
        page = paginator.paginate_queryset(queryset, request, view=self)

        if page is not None:
            serializer = GenerationRequestListSerializer(page, many=True, context={'existing_blobs_names': existing_blobs_names})
            return paginator.get_paginated_response(serializer.data)

        serializer = GenerationRequestListSerializer(queryset, many=True, context={'existing_blobs_names': existing_blobs_names})
        return Response(serializer.data, status=200)

    def retrieve(self, request, pk=None, *args, **kwargs):
        try:
            generation_request = GenerationRequest.objects.get(pk=pk, user=request.user)
        except GenerationRequest.DoesNotExist:
            return Response(status=404)

        if generation_request.is_hidden:
            return Response({"detail": "This generation is currently unavailable"}, status=400)

        serializer = GenerationRequestSerializer(generation_request)
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

        if generation_request.status == GenerationRequest.GenerationStatus.PROCESSING:
            return Response({"detail": "You cannot delete a generation that is currently in progress"}, status=400)

        try:
            services.delete_generation_request_images_from_gcs(generation_request)
            generation_request.delete()
            
            return Response(status=204)
        except Exception as e:
            logger.error(f"Failed to delete generation request", extra={'generation_request_id': generation_request.id, 'error': str(e)}, exc_info=True)
            return Response(status=400)

    @action(detail=False, methods=['GET'])
    def latest(self, request, *args, **kwargs):
        latest_user_generation_request = GenerationRequest.objects.filter(user=request.user).order_by('-created_at').first()

        if not latest_user_generation_request:
            return Response(status=204)
        
        if latest_user_generation_request.is_hidden:
            return Response({"detail": "This generation is currently unavailable"}, status=400)
        
        serializer = GenerationRequestSerializer(latest_user_generation_request)
        return Response(serializer.data, status=200)
    
    @action(detail=True, methods=['POST'])
    def stop(self, request, pk=None, *args, **kwargs):
        try:
            generation_request = GenerationRequest.objects.get(pk=pk, user=request.user, status=GenerationRequest.GenerationStatus.PROCESSING)
        except GenerationRequest.DoesNotExist:
            return Response({"detail": "Generation in progress not found or already stopped"}, status=404)

        try:
            generation_request.status = GenerationRequest.GenerationStatus.STOPPED_BY_USER
            generation_request.save(update_fields=['status', 'updated_at'])
            return Response(status=204)
        except Exception as e:
            logger.error(f"Failed to stop generation_request", extra={'generation_request_id': generation_request.id, 'error': str(e)}, exc_info=True)
            return Response(status=400)