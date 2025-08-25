from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from .models import TermsVersion, UserAgreement
from .serializers import TermsVersionSerializer
from .services import user_accept_documents_latest_version

@api_view(['GET'])
@permission_classes([AllowAny])
def published_agreements_list_view(request):
    document_types = TermsVersion.DocumentType.values
    latest_versions_qs = TermsVersion.objects.filter(
        document_type__in=document_types
    ).order_by('document_type', '-published_at').distinct('document_type')
    
    serializer = TermsVersionSerializer(latest_versions_qs, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def pending_agreements_list_view(request):
    user = request.user
    document_types = TermsVersion.DocumentType.values

    latest_versions_qs = TermsVersion.objects.filter(
        document_type__in=document_types
    ).order_by('document_type', '-published_at').distinct('document_type')
    
    latest_versions_map = {v.id: v for v in latest_versions_qs}
    if not latest_versions_map:
        return Response([])

    accepted_version_ids = set(
        UserAgreement.objects.filter(
            user=user,
            terms_version_id__in=latest_versions_map.keys()
        ).values_list('terms_version_id', flat=True)
    )

    pending_version_ids = set(latest_versions_map.keys()) - accepted_version_ids
    pending_agreements = [latest_versions_map[v_id] for v_id in pending_version_ids]

    serializer = TermsVersionSerializer(pending_agreements, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def accept_documents_latest_version(request):
    user_accept_documents_latest_version(request.user)

    return Response(status=204)