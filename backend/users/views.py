from rest_framework.decorators import api_view, permission_classes
from telegram_bot.services import send_message_to_user
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import UserProfile
from . import services
import logging

logger = logging.getLogger(__name__)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def credit_balance(request):
    user_profile = UserProfile.objects.get(user=request.user)
    total_credits = user_profile.free_credits + user_profile.paid_credits
    return Response({'credits': total_credits}, status=200)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_account(request):
    user = request.user
    telegram_id = user.profile.telegram_id
    language_code = request.data.get('language_code')
    success = services.delete_user_account(user)
    
    if success:
        try:
            send_message_to_user(
                telegram_id=telegram_id,
                message_key='account_deleted',
                language_code=language_code
            )
        except Exception as e:
            logger.error("Failed to send account deletion message", extra={'telegram_id': telegram_id, 'error': str(e)}, exc_info=True)

        return Response(status=204)
    else:
        return Response(status=400)