from .models import UserAgreement

def accept_user_document_version(user, terms_version, ip_address, user_agent, context):
    if UserAgreement.objects.filter(user=user, terms_version=terms_version).exists():
        return

    return UserAgreement.objects.create(
        user=user,
        terms_version=terms_version,
        ip_address=ip_address,
        user_agent=user_agent,
        context=context
    )