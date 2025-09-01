from .models import TermsVersion, UserAgreement

def user_accept_documents_latest_version(user):
    document_types = TermsVersion.DocumentType.values

    documents_latest_version_qs = TermsVersion.objects.filter(
        document_type__in=document_types
    ).order_by('document_type', '-published_at').distinct('document_type')
    
    documents_latest_version_map = {document_latest_version.id: document_latest_version for document_latest_version in documents_latest_version_qs}
    
    if not documents_latest_version_map:
        return

    accepted_documents_version_id = set(
        UserAgreement.objects.filter(
            user=user,
            terms_version_id__in=documents_latest_version_map.keys()
        ).values_list('terms_version_id', flat=True)
    )

    documents_version_id_to_create = set(documents_latest_version_map.keys()) - accepted_documents_version_id

    user_agreements_to_create = [
        UserAgreement(user=user, terms_version=documents_latest_version_map[document_version_id])
        for document_version_id in documents_version_id_to_create
    ]

    if user_agreements_to_create:
        UserAgreement.objects.bulk_create(user_agreements_to_create)