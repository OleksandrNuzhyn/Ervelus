from rest_framework.decorators import api_view, permission_classes, authentication_classes
from agreements.permissions import HasAcceptedLatestAgreements
from agreements.services import accept_user_document_version
from django.contrib.auth.models import update_last_login
from rest_framework.authtoken.models import Token
from generations.models import GenerationRequest
from rest_framework.permissions import AllowAny
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from agreements.models import TermsVersion
from asgiref.sync import async_to_sync
from users.models import UserProfile
from django.db import transaction
from django.conf import settings
from . import services
import telegram
import logging

bot = telegram.Bot(token=settings.TELEGRAM_API_KEY)
logger = logging.getLogger(__name__)
User = get_user_model()

@api_view(['POST'])
@authentication_classes([])
@permission_classes([AllowAny])
def telegram_auth(request):
    init_data = request.data.get('initData')

    if not init_data:
        logger.error("Telegram auth failed", extra={"reason": "no init_data provided"})
        return Response(status=400)

    try:
        telegram_data = services.validate_telegram_init_data(init_data)
    except Exception as e:
        logger.error("Telegram auth failed", extra={"reason": "validation error", "error": str(e)}, exc_info=True)
        return Response(status=400)

    telegram_id = str(telegram_data.get('id'))

    try:
        user_profile = UserProfile.objects.select_related('user').get(telegram_id=telegram_id)
        user = user_profile.user
    except UserProfile.DoesNotExist:
        try:
            user = create_telegram_user(telegram_data, request)
        except Exception as e:
            logger.error("Telegram auth failed", extra={"reason": "user creation error", "error": str(e)}, exc_info=True)
            return Response(status=400)

    if not user.is_active:
        return Response(status=400)

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
    
    try:
        chat_member = async_to_sync(bot.get_chat_member)(chat_id="-1003735555915", user_id=telegram_id)
        if chat_member.status == telegram.ChatMember.MEMBER:
            user_profile.free_credits += 1
            user_profile.is_subscribed = True
            user_profile.save(update_fields=['free_credits', 'is_subscribed'])
            
            services.send_message_to_user(
                telegram_id=telegram_id,
                message_key='subscription_bonus',
                language_code=telegram_data.get('language_code')
            )
    except Exception as e:
        logger.error("Failed to check channel subscription", extra={"error": str(e)}, exc_info=True)

    start_param = telegram_data.get('start_param')

    if start_param and start_param.startswith('ref_'):
        start_param_parts = start_param.split('_')

        if len(start_param_parts) == 2:
            inviter_telegram_id = start_param_parts[1]

            try:
                inviter_profile = UserProfile.objects.select_for_update().get(telegram_id=inviter_telegram_id)
                
                if inviter_profile.invited_count == 0:
                    inviter_profile.free_credits += 1
                    
                    services.send_message_to_user(
                        telegram_id=inviter_telegram_id,
                        message_key='referral_bonus',
                        language_code=telegram_data.get('language_code')
                    )

                inviter_profile.invited_count += 1
                inviter_profile.save(update_fields=['invited_count', 'free_credits'])
            except UserProfile.DoesNotExist:
                logger.error("Inviter not found while processing referral", extra={"telegram_id": inviter_telegram_id})
            except Exception as e:
                logger.error("Failed to process referral", extra={"error": str(e)}, exc_info=True)

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

@api_view(['GET'])
@permission_classes([HasAcceptedLatestAgreements])
def share_invite(request):
    try:
        language_code = request.META.get('HTTP_X_TELEGRAM_LANGUAGE', 'en')[:2]
        message = services.get_share_invite_message(telegram_id=request.user.profile.telegram_id, language_code=language_code)
        return Response({"message_id": message.id}, status=200)
    except Exception as e:
        logger.error("Failed to share invite", extra={"error": str(e)}, exc_info=True)
        return Response(status=400)

@api_view(['POST'])
@permission_classes([HasAcceptedLatestAgreements])
def share_generation(request):
    generation_id = request.data.get('generation_id')
    if not generation_id:
        return Response(status=400)

    try:
        generation_request = GenerationRequest.objects.get(
            pk=generation_id,
            user=request.user,
            status=GenerationRequest.GenerationStatus.COMPLETED
        )
    except GenerationRequest.DoesNotExist:
        return Response(status=404)

    try:
        language_code = request.META.get('HTTP_X_TELEGRAM_LANGUAGE', 'en')[:2]
        message = services.get_share_generation_message(
            telegram_id=request.user.profile.telegram_id,
            generation_request=generation_request,
            language_code=language_code
        )
        return Response({"message_id": message.id}, status=200)
    except Exception as e:
        logger.error("Failed to share generation", extra={"error": str(e)}, exc_info=True)
        return Response(status=400)