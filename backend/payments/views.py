from rest_framework.decorators import api_view, permission_classes
from agreements.permissions import HasAcceptedLatestAgreements
from rest_framework.response import Response
from products.models import StarPackage
from asgiref.sync import async_to_sync
from django.conf import settings
import telegram
import logging

logger = logging.getLogger(__name__)
bot = telegram.Bot(token=settings.TELEGRAM_API_KEY)

@api_view(['POST'])
@permission_classes([HasAcceptedLatestAgreements])
def create_star_invoice_link(request):
    star_package_id = request.data.get('star_package_id')

    if not star_package_id:
        return Response(status=400)
        
    try:
        star_package = StarPackage.objects.get(id=star_package_id)
    except StarPackage.DoesNotExist:
        return Response(status=404)
    
    try:
        country_code = request.user.profile.country_code
    except Exception:
        country_code = None

    amount = star_package.get_stars_count_for_country(country_code)
    payload = f"{star_package.generations_count}|{amount}"

    async def async_create_star_invoice_link():
        return await bot.create_invoice_link(
            title=star_package.name,
            description=star_package.name,
            payload=payload,
            currency="XTR",
            prices=[telegram.LabeledPrice(label=star_package.name, amount=amount)]
        )

    try:
        star_invoice_link = async_to_sync(async_create_star_invoice_link)()
    except Exception as e:
        logger.error(f"Failed to create star invoice link", extra={"error": str(e), "exc_info": True})
        return Response(status=400)
    
    if not star_invoice_link:
        logger.error(f"Star invoice link is empty")
        return Response(status=400)
        
    return Response({'star_invoice_link': star_invoice_link}, status=200)