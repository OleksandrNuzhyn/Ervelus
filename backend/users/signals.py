from django.dispatch import receiver
from allauth.socialaccount.signals import pre_social_login
from allauth.account.signals import email_confirmed
from allauth.account.models import EmailAddress
from django.contrib.auth import login

@receiver(pre_social_login)
def handle_social_login_verification(sender, request, sociallogin, **kwargs):
    if sociallogin.is_existing:
        user = sociallogin.user
        
        try:
            email_obj = EmailAddress.objects.get(user=user, primary=True)
            
            if not email_obj.verified:
                email_obj.verified = True
                email_obj.save()

        except EmailAddress.DoesNotExist:
            EmailAddress.objects.create(
                user=user,
                email=user.email,
                verified=True,
                primary=True,
            )

@receiver(email_confirmed)
def auto_login_on_email_confirmation(request, email_address, **kwargs):
    user = email_address.user
    login(request, user, backend='allauth.account.auth_backends.AuthenticationBackend')