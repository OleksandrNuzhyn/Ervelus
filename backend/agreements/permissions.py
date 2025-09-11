from rest_framework.permissions import BasePermission
from .models import TermsVersion, UserAgreement
from .serializers import TermsVersionSerializer
from .exceptions import UserAgreementsRequiredException
from django.db.models import Max


class HasAcceptedLatestAgreements(BasePermission):
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False

        required_document_types = [
            TermsVersion.DocumentType.TERMS_OF_SERVICE,
            TermsVersion.DocumentType.PRIVACY_POLICY
        ]

        latest_documents_version_qs = TermsVersion.objects.filter(
            document_type__in=required_document_types
        ).values('document_type').annotate(latest_document_version=Max('version'))

        if not latest_documents_version_qs:
            return True

        latest_documents_version_map = {
            item['document_type']: item['latest_document_version'] for item in latest_documents_version_qs
        }

        user_accepted_documents_version_qs = UserAgreement.objects.filter(
            user=request.user,
            terms_version__document_type__in=required_document_types
        ).values('terms_version__document_type').annotate(user_accepted_document_version=Max('terms_version__version'))

        user_accepted_documents_version_map = {
            item['terms_version__document_type']: item['user_accepted_document_version'] for item in user_accepted_documents_version_qs
        }

        user_document_types_to_accept = []

        for document_type, latest_document_version in latest_documents_version_map.items():
            user_accepted_document_version = user_accepted_documents_version_map.get(document_type)
            if user_accepted_document_version is None or user_accepted_document_version < latest_document_version:
                user_document_types_to_accept.append(document_type)

        if user_document_types_to_accept:
            user_documents_version_to_accept = TermsVersion.objects.filter(
                document_type__in=user_document_types_to_accept
            ).order_by('document_type', '-version').distinct('document_type')
            
            serializer = TermsVersionSerializer(user_documents_version_to_accept, many=True)
            raise UserAgreementsRequiredException(required_agreements=serializer.data)

        return True