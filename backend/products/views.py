from rest_framework.response import Response
from rest_framework.decorators import permission_classes, api_view
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import SubscriptionPlan, Style
from django.db.models import Exists, OuterRef, Subquery
from .serializers import StyleSerializer
from subscriptions.models import UserSubscription

@api_view(['GET'])
@permission_classes([AllowAny])
def subscription_plan_list(request):
    plans = SubscriptionPlan.objects.order_by('price').values(
        'name', 
        'description',
        'price',
        'paddle_price_id',
        'features',
        'is_active',
    )

    subscription_plan_list = list(plans)

    return Response(subscription_plan_list, status=200)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def available_style_list(request):
    user = request.user

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

    styles_list = list(styles_queryset)

    serializer = StyleSerializer(styles_list, many=True)
    return Response(serializer.data, status=200)