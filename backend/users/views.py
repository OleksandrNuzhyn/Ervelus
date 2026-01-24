from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.account.signals import user_signed_up
from django.dispatch import receiver
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.registration.views import SocialLoginView, VerifyEmailView
from dj_rest_auth.app_settings import api_settings
from dj_rest_auth.models import get_token_model
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from agreements.permissions import HasAcceptedLatestAgreements
from generations.models import GenerationRequest
from subscriptions.services import cancel_subscription
from rest_framework.response import Response
from django.contrib.contenttypes.models import ContentType
from .serializers import UserCreditsSerializer, SupportEmailSerializer
from .models import UserProfile
from auditlog.models import LogEntry
from auditlog.context import set_actor
from django.db import transaction
from . import services
import requests
import logging

logger = logging.getLogger(__name__)

@receiver(user_signed_up)
def user_signed_up_handler(request, user, **kwargs):
    request.is_registration = True


class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter
    client_class = OAuth2Client

    def get_response(self):
        response = super().get_response()
        response.data['is_registration'] = getattr(self.request, 'is_registration', False)
        return response

    def login(self):
        self.user = self.serializer.validated_data['user']
        token_model = get_token_model()
        
        if token_model:
            self.token = api_settings.TOKEN_CREATOR(token_model, self.user, self.serializer)


class CustomVerifyEmailView(VerifyEmailView):
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.kwargs['key'] = serializer.validated_data['key']
        confirmation = self.get_object()
        confirmation.confirm(self.request)
        
        user = confirmation.email_address.user
        token_model = get_token_model()

        if token_model:
            token = api_settings.TOKEN_CREATOR(token_model, user, serializer)
            token_serializer_class = api_settings.TOKEN_SERIALIZER
            response_data = token_serializer_class(token).data
            
            return Response(response_data, 200)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_credit_balance(request):
    user_profile = UserProfile.objects.annotate_total_credits().get(user=request.user)
    serializer = UserCreditsSerializer(user_profile)
    
    return Response(serializer.data, status=200)

@api_view(['POST'])
@permission_classes([AllowAny])
def send_support_email(request):
    try:
        serializer = SupportEmailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        sender_email = serializer.validated_data['email']
        text_body = serializer.validated_data['text_body']

        services.send_support_email(sender_email, text_body)

        return Response({"detail": "Support email successfully sent"}, status=200)
    except Exception as e:
        logger.error("Failed to send support email", extra={'error': str(e)}, exc_info=True)
        return Response({"detail": "Failed to send email"}, status=400)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def account_delete(request):
    user = request.user
    requests_in_process = GenerationRequest.objects.filter(user=user, is_visible=False)

    if requests_in_process.exists():
        logger.error("User deletion with unfinished generations", extra={'user_id': user.id, 'requests_in_process_ids': list(requests_in_process.values_list('id', flat=True))})

    active_subscriptions = user.subscriptions.filter(is_auto_renew=True)
    failed_subscriptions_cancellations = []

    for subscription in active_subscriptions:
        success = cancel_subscription(subscription)

        if not success:
            failed_subscriptions_cancellations.append(subscription.id)
            logger.error("Failed to auto-cancel subscription during account deletion", extra={'user_id': user.id, 'subscription_id': subscription.id})

    if failed_subscriptions_cancellations:
        return Response({"detail": f"Failed to cancel {len(failed_subscriptions_cancellations)} active subscriptions. Please contact support or try again later"}, status=400)
    
    related_objects_ids = []
    
    for obj in user.subscriptions.all():
        related_objects_ids.append((ContentType.objects.get_for_model(obj), str(obj.pk)))

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
        if e.response.status_code != 404:
            raise
    except requests.exceptions.RequestException as e:
        logger.error("Failed to remove user from Mailgun list in delete request due to HTTP error", extra={'user_id': user.id, 'error': str(e)}, exc_info=True)
        return Response(status=400)
    except Exception as e:
        logger.error("Failed to remove user from Mailgun list in delete request due to unknown error", extra={'user_id': user.id, 'error': str(e)}, exc_info=True)
        return Response(status=400)

    try:
        services.schedule_user_images_deletion(user)
    except Exception as e:
        logger.error("Failed to schedule user images deletion in delete request", extra={'user_id': user.id, 'error': str(e)}, exc_info=True)
        return Response(status=400)
    
    try:
        with transaction.atomic():
            user.auth_token.delete()

            for generation_request in user.generation_requests.all():
                generation_request.anonymise()

            for agreement in user.agreements.all():
                agreement.anonymise()

            for promo_code_usage in user.promo_code_usages.all():
                promo_code_usage.anonymise()
                
            user.socialaccount_set.all().delete()
            user.emailaddress_set.all().delete()

            if hasattr(user, 'profile'):
                user.profile.anonymise()
            user.anonymise()

            services.delete_user_audit_records(user, related_objects_ids)
    except Exception as e:
        logger.error("Failed to anonymise user data in delete request", extra={'user_id': user.id, 'error': str(e)}, exc_info=True)
        return Response(status=400)

    with set_actor(actor=None, remote_addr=None):
        LogEntry.objects.log_create(
            instance=user,
            action=LogEntry.Action.UPDATE,
            changes={},
            object_repr = f"Anonymised record of user_id: {user.pk}",
            additional_data={
                "gdpr_deletion_process": True,
                "message": "User data anonymization process completed"
            }
        )
    
    return Response(status=204)