from . import services
from adrf.decorators import api_view
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

@api_view(['POST'])
@permission_classes([IsAuthenticated])
async def customer_portal_session_create(request):
    try:
        portal_url = await services.create_customer_portal_session(request.user)
        return Response({'portal_url': portal_url}, status=201)
    except Exception:
        return Response(status=500)