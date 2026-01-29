from rest_framework.decorators import permission_classes, api_view
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.db.models import Value, BooleanField
from rest_framework.response import Response
from .serializers import StyleSerializer
from .models import Style, StarPackage

@api_view(['GET'])
@permission_classes([AllowAny])
def star_package_list(request):
    star_packages = StarPackage.objects.all().values('id', 'name', 'stars_count', 'generations_count')
    return Response(list(star_packages), status=200)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def available_style_list(request):
    styles_queryset = Style.objects.annotate(
        is_available=Value(True, output_field=BooleanField())
    ).select_related('genre').all()

    serializer = StyleSerializer(styles_queryset, many=True)
    return Response(serializer.data, status=200)