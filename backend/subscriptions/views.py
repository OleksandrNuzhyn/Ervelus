from rest_framework.decorators import api_view
from django.conf import settings
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from users.models import UserProfile
import requests
from .models import UserSubscription
from .serializers import UserSubscriptionListSerializer

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_subscription_list(request):
    user_subscriptions = UserSubscription.objects.select_related('plan').filter(user=request.user)
    serializer = UserSubscriptionListSerializer(user_subscriptions, many=True)

    try:
        profile = UserProfile.objects.get(user=request.user)

        if not profile.paddle_customer_id:
            return Response(None, status=204)

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
    except requests.RequestException:
        portal_url = None

    return Response({'subscriptions': serializer.data, 'portal_url': portal_url}, status=200)