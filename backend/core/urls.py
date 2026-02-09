from django.contrib import admin
from django_otp.admin import OTPAdminSite
from django.urls import path, include
from django.conf import settings


urlpatterns = []

if settings.DEBUG:
    urlpatterns += [
        path('sanekit/', admin.site.urls),
        path('webhooks/telegram/', include('telegram_bot.urls_webhooks')),
        path('webhooks/generations/', include('generations.urls_webhooks')),
        path('api/users/', include('users.urls')),
        path('api/payments/', include('payments.urls')),
        path('api/products/', include('products.urls')),
        path('api/generations/', include('generations.urls_api')),
        path('api/agreements/', include('agreements.urls')),
        path('api/marketing/', include('marketing.urls')),
        path('api/telegram/', include('telegram_bot.urls_api'))
    ]
else:
    admin.site.__class__ = OTPAdminSite
    
    if settings.SERVICE_NAME == 'ervelus-web-service':
        urlpatterns += [
            path('sanekit/', admin.site.urls),
            path('webhooks/telegram/', include('telegram_bot.urls_webhooks')),
            path('api/users/', include('users.urls')),
            path('api/payments/', include('payments.urls')),
            path('api/products/', include('products.urls')),
            path('api/generations/', include('generations.urls_api')),
            path('api/agreements/', include('agreements.urls')),
            path('api/marketing/', include('marketing.urls')),
            path('api/telegram/', include('telegram_bot.urls_api'))
        ]
    elif settings.SERVICE_NAME == 'ervelus-generations-service':
        urlpatterns += [
            path('webhooks/generations/', include('generations.urls_webhooks'))
        ]