from rest_framework.response import Response
from django.utils import timezone
from rest_framework.decorators import permission_classes, api_view
from rest_framework.permissions import AllowAny
from .models import SubscriptionPlan, Style
from django.db.models import Exists, OuterRef
from .serializers import StyleSerializer
from subscriptions.models import UserSubscription
from agreements.permissions import HasAcceptedLatestAgreements

@api_view(['GET'])
@permission_classes([AllowAny])
def subscription_plan_list(request):
    plans = SubscriptionPlan.objects.order_by('price').values(
        'id',
        'name', 
        'description',
        'price',
        'features',
        'is_active'
    )

    subscription_plan_list = list(plans)

    return Response(subscription_plan_list, status=200)

@api_view(['GET'])
@permission_classes([HasAcceptedLatestAgreements])
def available_style_list(request):
    target_plan_id = UserSubscription.objects.filter(
        user=request.user,
        end_time__gt=timezone.now()
    ).order_by('-plan__price').values_list('plan_id', flat=True).first()

    if not target_plan_id:
        target_plan_id = SubscriptionPlan.objects.order_by('price').values_list('id', flat=True).first()

    available_styles_subquery = SubscriptionPlan.unlocked_styles.through.objects.filter(
        style_id=OuterRef('pk'),
        subscriptionplan_id=target_plan_id
    )

    styles_queryset = Style.objects.annotate(
        is_available=Exists(available_styles_subquery)
    ).select_related('genre').all()

    serializer = StyleSerializer(styles_queryset, many=True)
    return Response(serializer.data, status=200)