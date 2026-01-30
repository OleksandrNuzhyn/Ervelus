from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from generations.models import GenerationRequest
from rest_framework.response import Response
from .models import UserProfile
from django.db import transaction
from . import services
import logging

logger = logging.getLogger(__name__)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_credit_balance(request):
    user_profile = UserProfile.objects.get(user=request.user)
    return Response({'credits': user_profile.credits}, status=200)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def account_delete(request):
    user = request.user
    requests_in_process = GenerationRequest.objects.filter(user=user, is_visible=False)

    if requests_in_process.exists():
        logger.error("User deletion with unfinished generations", extra={'user_id': user.id, 'requests_in_process_ids': list(requests_in_process.values_list('id', flat=True))})

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

            if hasattr(user, 'profile'):
                user.profile.anonymise()
            user.anonymise()
    except Exception as e:
        logger.error("Failed to anonymise user data in delete request", extra={'user_id': user.id, 'error': str(e)}, exc_info=True)
        return Response(status=400)

    return Response(status=204)