from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .models import UserSubscription
from .serializers import UserSubscriptionListSerializer, CreateOrderSerializer
from products.models import SubscriptionPlan
from core.models import ApplicationConfig
from agreements.permissions import HasAcceptedLatestAgreements
from django.db.models import Count, Sum
from datetime import datetime, timezone
from django.conf import settings
from . import services
import hmac
import hashlib
import time

@api_view(['POST'])
@permission_classes([HasAcceptedLatestAgreements])
def create_order(request):
    serializer = CreateOrderSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    plan_id = serializer.validated_data['plan_id']

    try:
        plan = SubscriptionPlan.objects.get(pk=plan_id, is_active=True)
    except SubscriptionPlan.DoesNotExist:
        return Response(status=404)
    
    budget_usage = UserSubscription.objects.filter(
        end_time__gt=datetime.now(timezone.utc)
    ).aggregate(
        total_cost=Sum('plan__product_price')
    )['total_cost'] or 0

    potential_spend = budget_usage + plan.product_price
    config = ApplicationConfig.get_solo()

    if potential_spend >= config.hard_budget:
        return Response(status=400)

    merchant_account = settings.WAYFORPAY_MERCHANT_ACCOUNT
    merchant_domain_name = settings.WAYFORPAY_MERCHANT_DOMAIN
    merchant_secret_key = settings.WAYFORPAY_SECRET_KEY

    user_id = request.user.id
    client_email = request.user.email
    readable_time = datetime.now(timezone.utc).strftime("%Y-%m-%d-%H-%M-%S-%f")
    order_reference = f"{user_id}_{plan_id}_{readable_time}"
    order_date = str(int(time.time()))
    amount = str(plan.price)
    currency = "USD"
    product_name = plan.name
    product_count = str(1)
    product_price = str(plan.price)

    string_for_sign = f"{merchant_account};{merchant_domain_name};{order_reference};{order_date};{amount};{currency};{product_name};{product_count};{product_price}"
    
    merchant_signature = hmac.new(
        merchant_secret_key.encode('utf-8'),
        string_for_sign.encode('utf-8'),
        hashlib.md5
    ).hexdigest()

    return Response({
        'merchantAccount': merchant_account,
        'merchantDomainName': merchant_domain_name,
        'merchantSignature': merchant_signature,
        'orderReference': order_reference,
        'orderDate': order_date,
        'amount': amount,
        'currency': currency,
        'productName': [product_name],
        'productCount': [product_count],
        'productPrice': [product_price],
        'clientEmail': client_email,
        'regularBehavior': 'preset',
        'regularMode': 'monthly',
        'regularCount': '11',
        'language': 'EN'
    }, status=200)

@api_view(['GET'])
@permission_classes([HasAcceptedLatestAgreements])
def user_subscription_list(request):
    user_subscriptions = UserSubscription.objects.select_related('plan').filter(
        user=request.user
    ).annotate(
        plan_unlocked_styles_count=Count('plan__unlocked_styles')
    ).order_by('start_time')

    serializer = UserSubscriptionListSerializer(user_subscriptions, many=True)
    return Response({'subscriptions': serializer.data}, status=200)

@api_view(['POST'])
@permission_classes([HasAcceptedLatestAgreements])
def cancel_subscription(request, id):
    try:
        subscription = UserSubscription.objects.get(id=id, user=request.user)
    except UserSubscription.DoesNotExist:
        return Response(status=404)
    
    success = services.cancel_subscription(subscription)
    
    if success:
        return Response(status=200)
    
    return Response(status=400)