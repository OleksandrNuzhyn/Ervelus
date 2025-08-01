import json
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import GenerationRequest
from .serializers import GenerationRequestCreateSerializer, GenerationRequestOutputSerializer
from google.pubsub_v1.services.publisher.async_client import PublisherAsyncClient
from asgiref.sync import sync_to_async
from . import services
from django.conf import settings

publisher = PublisherAsyncClient()


class GenerationRequestViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return GenerationRequest.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action == 'create':
            return GenerationRequestCreateSerializer
        return GenerationRequestOutputSerializer

    async def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        await sync_to_async(serializer.is_valid)(raise_exception=True)

        input_image_file = serializer.validated_data['input_image']
        
        input_image_url = await services.upload_image_to_gcs(
            image_file=input_image_file, 
            user_id=request.user.id, 
            image_source='input'
        )
        
        generation_request = await GenerationRequest.objects.acreate(
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
            await publisher.publish(topic_path, json.dumps(event_data).encode('utf-8'))
        except Exception:
            return Response({"error": "Failed to publish generation task"}, status=500)

        serializer = GenerationRequestOutputSerializer(generation_request)
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