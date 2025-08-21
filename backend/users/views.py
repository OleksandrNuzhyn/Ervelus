import hashlib
import logging
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.registration.views import SocialLoginView
from rest_framework.decorators import api_view, permission_classes
from django.views.decorators.csrf import ensure_csrf_cookie
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from generations.models import GenerationRequest
from . import services
from .serializers import UserCreditsSerializer
from .models import UserProfile

logger = logging.getLogger(__name__)


class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter
    client_class = OAuth2Client


@api_view(['GET'])
@permission_classes([AllowAny])
@ensure_csrf_cookie
def csrf_token(request):
    return Response(status=204)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_credit_balance(request):
    user_profile = UserProfile.objects.annotate_total_credits().get(user=request.user)
    serializer = UserCreditsSerializer(user_profile)
    
    return Response(serializer.data, status=200)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def account_delete(request):
    user = request.user
    user_id = user.id
    email_hash = hashlib.sha256(user.email.encode('utf-8')).hexdigest()

    try:
        if GenerationRequest.objects.filter(user=user, status=GenerationRequest.GenerationStatus.PROCESSING).exists():
            logger.warning(f"User deletion blocked due to processing generation. user_id='{user_id}'")
            return Response({"detail": "You have generations in progress. Please wait for them to complete before deleting your account"}, status=400)
        
        if not user.profile.paddle_customer_id:
            services.delete_user_images_from_gcs(user_id)
            user.delete()
            logger.info(f"User account deleted successfully. user_id='{user_id}', email_hash='{email_hash}'")
            
            return Response(status=204)

        customer_id = user.profile.paddle_customer_id
        uncancelled_subscriptions = services.get_user_uncancelled_paddle_subscriptions(customer_id)

        if not uncancelled_subscriptions:
            services.delete_user_images_from_gcs(user_id)
            user.delete()
            logger.info(f"User account deleted successfully. user_id='{user_id}', email_hash='{email_hash}'")

            return Response(status=204)

        portal_url = services.create_customer_portal_session(customer_id)
        logger.warning(f"User deletion blocked due to found {len(uncancelled_subscriptions)} uncancelled subscriptions. user_id='{user_id}'")
        
        return Response({
            "detail": f"You have {len(uncancelled_subscriptions)} uncancelled subscriptions. Please cancel them before deleting your account", 
            "customer_portal_url": portal_url
        }, status=400)
    except Exception as e:
        logger.error(f"Failed to delete account. user_id='{user_id}', error='{e}'", exc_info=True)
        return Response({"error": "Failed to delete account"}, status=500)