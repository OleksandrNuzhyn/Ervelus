from django.conf import settings
from django.shortcuts import redirect
from allauth.account.views import ConfirmEmailView


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