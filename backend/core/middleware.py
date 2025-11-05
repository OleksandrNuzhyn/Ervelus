from django.conf import settings
from django.http import JsonResponse


class MaintenanceModeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not settings.MAINTENANCE_MODE:
            return self.get_response(request)

        excluded_paths = [
            '/sanekit/',
            '/webhooks/subscriptions/'
        ]

        if any(request.path.startswith(path) for path in excluded_paths):
            return self.get_response(request)
            
        return JsonResponse({"maintenance_mode": True}, status=503)