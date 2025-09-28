from rest_framework.decorators import api_view, permission_classes
from django.conf import settings
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .models import UserSubscription
from .serializers import UserSubscriptionListSerializer, SubscriptionEligibilityCheckSerializer
from products.models import SubscriptionPlan
from core.models import ApplicationConfig
from agreements.permissions import HasAcceptedLatestAgreements
import requests
import logging

logger = logging.getLogger(__name__)

@api_view(['POST'])
@permission_classes([AllowAny])
def subscription_eligibility_check(request):
    serializer = SubscriptionEligibilityCheckSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    plan_id = serializer.validated_data['plan_id']

    try:
        plan = SubscriptionPlan.objects.get(pk=plan_id, is_active=True)
    except SubscriptionPlan.DoesNotExist:
        return Response({'detail': 'Plan is not active now'}, status=400)

    config = ApplicationConfig.get_solo()

    potential_spend = config.reserved_for_spend + plan.product_price
    if potential_spend >= config.hard_budget:
        return Response({'detail': 'Purchase unavailable due to budget limits. We apologize for the inconvenience — improvements are underway'}, status=400)

    return Response(status=200)

@api_view(['GET'])
@permission_classes([HasAcceptedLatestAgreements])
def user_subscription_list(request):
    user_subscriptions = UserSubscription.objects.select_related('plan').filter(user=request.user)
    serializer = UserSubscriptionListSerializer(user_subscriptions, many=True)
    profile = request.user.profile
    portal_url = None

    try:
        if profile.paddle_customer_id:
            paddle_customer_id = profile.paddle_customer_id
            url = f"{settings.PADDLE_API_BASE_URL.rstrip('/')}/customers/{paddle_customer_id}/portal-sessions"
            headers = {
                "Authorization": f"Bearer {settings.PADDLE_API_KEY}",
                "Content-Type": "application/json",
            }

            response = requests.post(url, headers=headers)
            response.raise_for_status()

            response_data = response.json()
            portal_url = response_data['data']['urls']['general']['overview']
    except requests.RequestException as e:
        logger.error("Failed to create customer portal session due to HTTP error", extra={'user_id': request.user.id, 'error': str(e)}, exc_info=True)
    except Exception as e:
        logger.error("Failed to create customer portal session due to unknown error", extra={'user_id': request.user.id, 'error': str(e)}, exc_info=True)
        portal_url = None

    return Response({'subscriptions': serializer.data, 'portal_url': portal_url}, status=200)