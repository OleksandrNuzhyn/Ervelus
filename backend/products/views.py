from rest_framework.response import Response
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny
from adrf.decorators import api_view
from .models import SubscriptionPlan


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