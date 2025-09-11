from .serializers import TermsVersionSerializer, AcceptUserDocumentVersionSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from .services import accept_user_document_version
from rest_framework.response import Response
from .models import TermsVersion

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def accept_user_document_version_client_side(request):
    serializer = AcceptUserDocumentVersionSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    terms_version_id = serializer.validated_data['terms_version_id']

    try:
        terms_version = TermsVersion.objects.get(id=terms_version_id)
    except TermsVersion.DoesNotExist:
        return Response({'detail': 'Not found'}, status=404)

    ip_address = request.META.get('REMOTE_ADDR')
    user_agent = request.META.get('HTTP_USER_AGENT')
    context = {"source": "terms_update_modal", "method": "checkbox"}

    accept_user_document_version(
        user=request.user,
        terms_version=terms_version,
        ip_address=ip_address,
        user_agent=user_agent,
        context=context
    )

    return Response(status=201)




@api_view(['GET'])
@permission_classes([AllowAny])
def published_agreements_list_view(request):
    document_types = TermsVersion.DocumentType.values
    latest_versions_qs = TermsVersion.objects.filter(
        document_type__in=document_types
    ).order_by('document_type', '-published_at').distinct('document_type')
    
    serializer = TermsVersionSerializer(latest_versions_qs, many=True)
    return Response(serializer.data)