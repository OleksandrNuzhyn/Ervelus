from rest_framework.decorators import permission_classes, api_view
from rest_framework.permissions import IsAuthenticated
from django.db.models import Value, BooleanField
from rest_framework.response import Response
from .serializers import StyleSerializer
from .models import Style, StarPackage

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def star_package_list(request):
    country_code = request.user.profile.country_code
    star_packages_queryset = StarPackage.objects.filter(is_active=True)
    star_packages = []

    for star_package in star_packages_queryset:
        stars_counts_dict = star_package.stars_counts or {}
        stars_count = None

        if country_code:
            stars_count = stars_counts_dict.get(country_code)
        
        if stars_count is None:
            stars_count = stars_counts_dict.get('default')
            
        if stars_count is not None:
            star_packages.append({
                'id': star_package.id,
                'name': star_package.name,
                'stars_count': stars_count,
                'generations_count': star_package.generations_count
            })
    
    return Response({'star_packages': star_packages}, status=200)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def available_style_list(request):
    styles_queryset = Style.objects.annotate(
        is_available=Value(True, output_field=BooleanField())
    ).select_related('genre').all()

    serializer = StyleSerializer(styles_queryset, many=True)
    return Response(serializer.data, status=200)