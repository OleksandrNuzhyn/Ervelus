from rest_framework.decorators import api_view
from django.conf import settings
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from users.models import UserProfile
import requests

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def customer_portal_session_create(request):
    try:
        profile = UserProfile.objects.get(user=request.user)

        if not profile.paddle_customer_id:
            raise Exception()

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
        return Response({'portal_url': portal_url}, status=201)
    except Exception:
        return Response(status=500)