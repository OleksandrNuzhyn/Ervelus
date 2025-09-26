from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.registration.views import SocialLoginView
from rest_framework.decorators import api_view, permission_classes
from django.views.decorators.csrf import ensure_csrf_cookie
from rest_framework.permissions import AllowAny, IsAuthenticated
from agreements.permissions import HasAcceptedLatestAgreements
from generations.models import GenerationRequest
from rest_framework.response import Response
from .serializers import UserCreditsSerializer
from .models import UserProfile
from auditlog.models import LogEntry
from django.db import transaction
from . import services
import requests
import logging

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
@permission_classes([HasAcceptedLatestAgreements])
def user_credit_balance(request):
    user_profile = UserProfile.objects.annotate_total_credits().get(user=request.user)
    serializer = UserCreditsSerializer(user_profile)
    
    return Response(serializer.data, status=200)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def account_delete(request):
    user = request.user

    if GenerationRequest.objects.filter(user=user, status=GenerationRequest.GenerationStatus.PROCESSING).exists():
        return Response({"detail": "You have generation requests in progress. Please wait for them to complete or stop before deleting your account"}, status=400)

    if user.profile.paddle_customer_id:
        try:
            paddle_customer_id = user.profile.paddle_customer_id
            uncancelled_subscriptions = services.get_user_uncancelled_paddle_subscriptions(paddle_customer_id)

            if uncancelled_subscriptions:
                portal_url = services.create_customer_portal_session(paddle_customer_id)
                return Response({
                    "detail": f"You have {len(uncancelled_subscriptions)} uncancelled subscriptions. Please cancel them before deleting your account",
                    "portal_url": portal_url
                }, status=400)
        except requests.RequestException as e:
            logger.error("Failed to parse user uncancelled subscriptions in delete request due to HTTP error", extra={'user_id': user.id, 'error': str(e)}, exc_info=True)
            return Response(status=400)
        except Exception as e:
            logger.error("Failed to parse user uncancelled subscriptions in delete request due to unknown error", extra={'user_id': user.id, 'error': str(e)}, exc_info=True)
            return Response(status=400)

    LogEntry.objects.log_create(
        instance=user,
        action=LogEntry.Action.ACCESS,
        changes={},
        additional_data={
            "gdpr_deletion_process": True,
            "message": "User data anonymization process started"
        }
    )
    
    try:
        user_data_for_retention = services.get_user_data_for_retention(user)
    except Exception as e:
        logger.error("Failed to get user data for retention in delete request", extra={'user_id': user.id, 'error': str(e)}, exc_info=True)
        return Response(status=400)

    try:
        services.upload_user_data_for_retention_to_gcs(user, user_data_for_retention)
    except Exception as e:
        logger.error("Failed to upload user data for retention to GCS in delete request", extra={'user_id': user.id, 'error': str(e)}, exc_info=True)
        return Response(status=400)

    try:
        services.remove_user_from_mailgun_list(user)
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 404:
            logger.info("User was not found in Mailgun list in delete request", extra={'user_id': user.id})
        else:
            raise
    except requests.exceptions.RequestException as e:
        logger.error("Failed to remove user from Mailgun list in delete request due to HTTP error", extra={'user_id': user.id, 'error': str(e)}, exc_info=True)
        return Response(status=400)
    except Exception as e:
        logger.error("Failed to remove user from Mailgun list in delete request due to unknown error", extra={'user_id': user.id, 'error': str(e)}, exc_info=True)
        return Response(status=400)

    try:
        if user.profile.paddle_customer_id:
            services.archive_paddle_customer(user)
    except requests.exceptions.RequestException as e:
        logger.error("Failed to archive user in Paddle in delete request due to HTTP error", extra={'user_id': user.id, 'error': str(e)}, exc_info=True)
        return Response(status=400)
    except Exception as e:
        logger.error("Failed to archive user in Paddle in delete request due to unknown error", extra={'user_id': user.id, 'error': str(e)}, exc_info=True)
        return Response(status=400)

    try:
        deletion_report = services.delete_user_images_from_gcs(user)

        deleted_originals = deletion_report.get('deleted_original_count', 0)
        deleted_resized = deletion_report.get('deleted_resized_count', 0)

        if deleted_originals != deleted_resized:
            logger.error("Mismatch in deleted image counts from GCS", extra={'user_id': user.id, 'deleted_originals': deleted_originals, 'deleted_resized': deleted_resized})
    except Exception as e:
        logger.error("Failed to delete user images from GCS in delete request", extra={'user_id': user.id, 'error': str(e)}, exc_info=True)
        return Response(status=400)
    
    try:
        with transaction.atomic():
            user.generation_requests.all().anonymise()
            user.agreements.all().anonymise()
            user.socialaccount_set.all().delete()
            user.emailaddress_set.all().delete()

            user.anonymise()

            services.delete_user_audit_records(user)
    except Exception as e:
        logger.error("Failed to anonymise user data in delete request", extra={'user_id': user.id, 'error': str(e)}, exc_info=True)
        return Response(status=400)

    LogEntry.objects.log_create(
        instance=user,
        action=LogEntry.Action.UPDATE,
        changes={},
        additional_data={
            "gdpr_deletion_process": True,
            "message": "User data anonymization process completed"
        }
    )
    
    return Response(status=204)