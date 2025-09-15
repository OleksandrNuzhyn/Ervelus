import hashlib
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.registration.views import SocialLoginView
from rest_framework.decorators import api_view, permission_classes
from django.views.decorators.csrf import ensure_csrf_cookie
from rest_framework.permissions import AllowAny, IsAuthenticated
from agreements.permissions import HasAcceptedLatestAgreements
from rest_framework.response import Response
from .serializers import UserCreditsSerializer
from .models import UserProfile
from auditlog.models import LogEntry
from . import services


class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter
    client_class = OAuth2Client


@api_view(['GET'])
@permission_classes([AllowAny])
@ensure_csrf_cookie
def csrf_token(request):
    return Response(status=204)

@api_view(['GET'])
@permission_classes([HasAcceptedLatestAgreements])
def user_credit_balance(request):
    user_profile = UserProfile.objects.annotate_total_credits().get(user=request.user)
    serializer = UserCreditsSerializer(user_profile)
    
    return Response(serializer.data, status=200)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def account_delete(request):
    user = request.user
    
    if hasattr(user, 'profile') and user.profile.paddle_customer_id:
        paddle_customer_id = user.profile.paddle_customer_id
        uncancelled_subscriptions = services.get_user_uncancelled_paddle_subscriptions(paddle_customer_id)

        if uncancelled_subscriptions:
            portal_url = services.create_customer_portal_session(paddle_customer_id)
            return Response({
                "detail": f"You have {len(uncancelled_subscriptions)} uncancelled subscriptions. Please cancel them before deleting your account",
                "customer_portal_url": portal_url
            }, status=400)

    services.remove_user_from_mailgun_list(user)
    services.archive_paddle_customer(user)
    services.delete_user_images_from_gcs(user)
    
    user_data_for_retention = services.get_user_data_for_retention(user)
    services.upload_user_data_for_retention_to_gcs(user, user_data_for_retention)

    user.generation_requests.all().anonymise()
    user.agreements.all().anonymise()
    user.socialaccount_set.all().delete()
    user.emailaddress_set.all().delete()
    user.anonymise()

    services.delete_user_audit_records(user)

    LogEntry.objects.log_create(
        instance=user,
        action=LogEntry.Action.UPDATE,
        changes='User account data anonymized after data retention',
        additional_data={"gdpr_deletion_process": True}
    )
    
    return Response(status=204)