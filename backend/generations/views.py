import json
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from .models import GenerationRequest
from . import services
from .serializers import GenerationRequestCreateSerializer, GenerationRequestSerializer
from google.cloud import pubsub_v1
from django.conf import settings

publisher = pubsub_v1.PublisherClient()


class GenerationRequestViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = GenerationRequestCreateSerializer(data=request.data)
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
            topic_path = publisher.topic_path(settings.GCP_PROJECT_ID, settings.GCP_PUBSUB_GENERATION_EVENTS_TOPIC_ID)
            event_data = {
                'generation_request_id': generation_request.id,
                'resolution': serializer.validated_data['resolution']
            }
            future = publisher.publish(topic_path, json.dumps(event_data).encode('utf-8'))
            future.result()
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
