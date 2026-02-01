from django.contrib.auth import get_user_model
from django.contrib.auth.models import update_last_login
from rest_framework.decorators import api_view, permission_classes
from agreements.services import accept_user_document_version
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from agreements.models import TermsVersion
from core.models import ApplicationConfig
from users.models import UserProfile
from django.db import transaction
from django.db.models import F
from . import services
import logging

logger = logging.getLogger(__name__)
User = get_user_model()

@api_view(['POST'])
@permission_classes([AllowAny])
def telegram_auth(request):
    init_data = request.data.get('initData')

    if not init_data:
        logger.error("Telegram auth failed", extra={"reason": "no init_data provided"})
        return Response({"detail": "Authentication failed"}, status=400)

    try:
        telegram_data = services.validate_telegram_init_data(init_data)
    except Exception as e:
        logger.error("Telegram auth failed", extra={"reason": "validation error", "error": str(e)}, exc_info=True)
        return Response({"detail": "Authentication failed"}, status=400)

    telegram_id = str(telegram_data.get('id'))

    try:
        user_profile = UserProfile.objects.select_related('user').get(telegram_id=telegram_id)
        user = user_profile.user
    except UserProfile.DoesNotExist:
        try:
            user = create_telegram_user(telegram_data, request)
        except Exception as e:
            logger.error("Telegram auth failed", extra={"reason": "user creation error", "error": str(e)}, exc_info=True)
            return Response({"detail": "Authentication failed"}, status=400)

    token, _ = Token.objects.get_or_create(user=user)
    update_last_login(None, user)
    
    return Response({'token': token.key}, status=200)

@transaction.atomic
def create_telegram_user(telegram_data, request):
    telegram_id = str(telegram_data.get('id'))
    email = f"tg_{telegram_id}@tma.ervelus.com"

    user = User.objects.create_user(
        username=f"tg_{telegram_id}",
        email=email,
        password=None,
        first_name=telegram_data.get('first_name', ''),
        last_name=telegram_data.get('last_name', '')
    )
    user.set_unusable_password()
    user.save()

    ip_address = request.META.get('HTTP_X_FORWARDED_FOR', '').split(',')[0].strip()
    country_code = services.get_country_code_from_ip_address(ip_address)

    user_profile = UserProfile.objects.create(user=user, telegram_id=telegram_id, country_code=country_code)
    
    config = ApplicationConfig.get_solo()
    config.reserved_generations = F('reserved_generations') + user_profile.credits
    config.save(update_fields=['reserved_generations'])

    required_document_types = [
        TermsVersion.DocumentType.TERMS_OF_SERVICE,
        TermsVersion.DocumentType.PRIVACY_POLICY
    ]

    latest_documents_version_to_accept = TermsVersion.objects.filter(
        document_type__in=required_document_types
    ).order_by('document_type', '-version').distinct('document_type')

    if len(latest_documents_version_to_accept) != len(required_document_types):
        raise Exception("Cannot auto-accept terms. Not all required documents are found")

    ip_address = request.META.get('HTTP_X_FORWARDED_FOR', '').split(',')[0].strip()
    user_agent = request.META.get('HTTP_USER_AGENT', '')
    context = {"source": "tma", "method": "automatic"}

    for latest_document_version_to_accept in latest_documents_version_to_accept:
        accept_user_document_version(
            user=user,
            terms_version=latest_document_version_to_accept,
            ip_address=ip_address,
            user_agent=user_agent,
            context=context
        )
    
    return user