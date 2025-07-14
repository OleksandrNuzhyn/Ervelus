from django.dispatch import receiver
from allauth.socialaccount.signals import pre_social_login
from allauth.account.models import EmailAddress

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
                primary=True
            ) 