from rest_framework.decorators import permission_classes, api_view
from django.db.models import Value, BooleanField, Case, When
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .serializers import StyleSerializer
from .models import Style, StarPackage

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def store(request):
    star_packages_queryset = StarPackage.objects.filter(is_active=True)
    star_packages = []

    for star_package in star_packages_queryset:
        star_packages.append({
            'id': star_package.id,
            'name': star_package.name,
            'stars_count': star_package.stars_count_t1,
            'generations_count': star_package.generations_count
        })
    
    return Response({
        'star_packages': star_packages,
        'is_subscribed': request.user.profile.is_subscribed,
        'invited_count': request.user.profile.invited_count
    }, status=200)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def style_list(request):
    is_paid = request.user.profile.is_paid

    styles_queryset = Style.objects.annotate(
        is_available=Case(
            When(is_paid=False, then=Value(True)),
            When(is_paid=True, then=Value(is_paid)),
            output_field=BooleanField()
        )
    ).select_related('genre').all()

    serializer = StyleSerializer(styles_queryset, many=True)
    return Response(serializer.data, status=200)