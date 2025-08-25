from django.http import JsonResponse
from django.urls import reverse
from .models import TermsVersion, UserAgreement


class AgreementCheckMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.user.is_authenticated or request.path.startswith('/admin/'):
            return self.get_response(request)

        excluded_paths = [
            reverse('agreements:pending-list'),
            reverse('agreements:accept')
        ]
        if request.path in excluded_paths:
            return self.get_response(request)

        document_types = TermsVersion.DocumentType.values
        documents_latest_version = self.get_documents_latest_version(document_types)
        
        if not documents_latest_version:
            return self.get_response(request)

        accepted_documents_version_id = self.get_user_accepted_documents_version(request.user, documents_latest_version)

        if len(accepted_documents_version_id) < len(document_types):
            #return JsonResponse({'message': 'User has not accepted all required agreements'}, status=428)
            pass

        return self.get_response(request)

    def get_documents_latest_version(self, document_types):
        documents_latest_version_qs = TermsVersion.objects.filter(
            document_type__in=document_types
        ).order_by('document_type', '-published_at').distinct('document_type')

        return {document_latest_version.document_type: document_latest_version for document_latest_version in documents_latest_version_qs}

    def get_user_accepted_documents_version(self, user, documents_latest_version):
        return set(
            UserAgreement.objects.filter(
                user=user,
                terms_version__id__in=[document_latest_version.id for document_latest_version in documents_latest_version.values()]
            ).values_list('terms_version__id', flat=True)
        )