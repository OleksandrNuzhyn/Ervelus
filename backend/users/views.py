from django.conf import settings
from django.shortcuts import redirect
from allauth.account.views import ConfirmEmailView
from dj_rest_auth.views import PasswordResetConfirmView
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from dj_rest_auth.registration.views import SocialLoginView


class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter


class ConfirmEmailRedirectView(ConfirmEmailView):
    template_name = None

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.confirm(request)

        redirect_url = getattr(
            settings,
            "ACCOUNT_EMAIL_CONFIRMATION_ANONYMOUS_REDIRECT_URL",
        )
        return redirect(redirect_url)


class PasswordResetRedirectView(PasswordResetConfirmView):
    def post(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)

        redirect_url = getattr(
            settings,
            "PASSWORD_RESET_REDIRECT_URL",
        )
        return redirect(redirect_url)