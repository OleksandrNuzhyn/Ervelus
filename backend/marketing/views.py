from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from agreements.permissions import HasAcceptedLatestAgreements
from .models import PromoCode, PromoCodeUsage
from .serializers import ApplyPromoCodeSerializer
from core.models import ApplicationConfig
from django.db import transaction
from django.db.models import F

@api_view(['POST'])
@permission_classes([HasAcceptedLatestAgreements])
def apply_promo_code(request):
    serializer = ApplyPromoCodeSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    
    code = serializer.validated_data['code']
    user = request.user
    
    try:
        promo_code = PromoCode.objects.get(code__iexact=code)
    except PromoCode.DoesNotExist:
        return Response({"detail": "This promo code does not exist"}, status=404)
    
    if not promo_code.is_active:
        return Response({"detail": "This promo code is no longer active"}, status=400)
    
    if promo_code.current_usages >= promo_code.max_usages:
        return Response({"detail": "This promo code has reached usage limit"}, status=400)
    
    if PromoCodeUsage.objects.filter(user=user, promo_code=promo_code).exists():
        return Response({"detail": "You have already used this promo code"}, status=400)
    
    try:
        with transaction.atomic():
            PromoCodeUsage.objects.create(user=user, promo_code=promo_code)
            
            user.profile.credits += promo_code.credits_count
            user.profile.save(update_fields=['credits'])
            
            promo_code.current_usages += 1
            promo_code.save(update_fields=['current_usages'])
            
            config = ApplicationConfig.get_solo()
            config.reserved_generations = F('reserved_generations') + promo_code.credits_count
            config.save(update_fields=['reserved_generations'])
    except Exception:
        return Response({"detail": "Failed to apply promo code. Please try again"}, status=400)
    
    return Response({'credits_count': promo_code.credits_count}, status=200)