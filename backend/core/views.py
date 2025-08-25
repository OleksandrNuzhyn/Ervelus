from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .models import ApplicationConfig
from .serializers import ApplicationConfigSerializer

@api_view(['GET'])
@permission_classes([AllowAny])
def app_config_details(request):
    config = ApplicationConfig.get_solo()
    serializer = ApplicationConfigSerializer(config)

    return Response(serializer.data, status=200)