from rest_framework.response import Response
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from adrf.decorators import api_view
from asgiref.sync import sync_to_async
from .models import SubscriptionPlan, Style
from django.db.models import Exists, OuterRef, Subquery
from .serializers import StyleSerializer
from subscriptions.models import UserSubscription

@api_view(['GET'])
@permission_classes([AllowAny])
async def subscription_plan_list(request):
    plans = SubscriptionPlan.objects.values(
        'name', 
        'description',
        'price',
        'paddle_price_id',
        'features',
        'is_active',
    )

    subscription_plan_list = [plan async for plan in plans]

    return Response(subscription_plan_list, status=200)

@sync_to_async
def get_styles_list(user):
    best_plan_id_subquery = UserSubscription.objects.filter(
        user=user,
        status=UserSubscription.SubscriptionStatus.ACTIVE
    ).order_by('-plan__price').values('plan_id')[:1]

    available_styles_subquery = SubscriptionPlan.unlocked_styles.through.objects.filter(
        style_id=OuterRef('pk'),
        subscriptionplan_id=Subquery(best_plan_id_subquery)
    )

    styles_queryset = Style.objects.annotate(
        is_available=Exists(available_styles_subquery)
    ).select_related('genre').all()
    
    return list(styles_queryset)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
async def available_style_list(request):
    user = request.user
    styles_list = await get_styles_list(user)

    serializer = StyleSerializer(styles_list, many=True)
    return Response(serializer.data, status=200)