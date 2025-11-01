from rest_framework.throttling import ScopedRateThrottle


THROTTLE_SCOPES_MAP = {
    # auth
    'rest_login': 'auth_anon',
    'rest_password_reset': 'auth_anon',
    'rest_password_reset_confirm': 'auth_anon',
    'google-login': 'auth_anon',

    # registration
    'rest_register': 'auth_anon',
    'rest_verify_email': 'auth_anon',
    'rest_resend_email': 'auth_anon',

    # contact
    'send-support-email': 'contact_anon',
}


class CustomScopedRateThrottle(ScopedRateThrottle):
    def allow_request(self, request, view):
        url_name = request.resolver_match.url_name
        self.scope = THROTTLE_SCOPES_MAP.get(url_name)

        if not self.scope:
            return True

        self.rate = self.get_rate()
        self.num_requests, self.duration = self.parse_rate(self.rate)

        return super(ScopedRateThrottle, self).allow_request(request, view)