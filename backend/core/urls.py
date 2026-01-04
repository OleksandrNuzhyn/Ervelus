from django.contrib import admin
from django_otp.admin import OTPAdminSite
from django.urls import path, include
from django.conf import settings
from . import views


urlpatterns = []

if settings.DEBUG:
    urlpatterns += [
        path('sanekit/', admin.site.urls),
        
        path('webhooks/subscriptions/', include('subscriptions.urls_webhooks')),
        path('webhooks/generations/', include('generations.urls_webhooks')),

        path('api/auth/', include('users.urls')),
        path('api/core/app-config/', views.app_config_details, name='app-config-details'),
        path('api/subscriptions/', include('subscriptions.urls_api')),
        path('api/products/', include('products.urls')),
        path('api/generations/', include('generations.urls_api')),
        path('api/agreements/', include('agreements.urls')),
        path('api/marketing/', include('marketing.urls'))
    ]
else:
    admin.site.__class__ = OTPAdminSite
    
    if settings.SERVICE_NAME == 'ervelus-web-service':
        urlpatterns += [
            path('sanekit/', admin.site.urls),

            path('webhooks/subscriptions/', include('subscriptions.urls_webhooks')),

            path('api/auth/', include('users.urls')),
            path('api/core/app-config/', views.app_config_details, name='app-config-details'),
            path('api/subscriptions/', include('subscriptions.urls_api')),
            path('api/products/', include('products.urls')),
            path('api/generations/', include('generations.urls_api')),
            path('api/agreements/', include('agreements.urls')),
            path('api/marketing/', include('marketing.urls'))
        ]
    elif settings.SERVICE_NAME == 'ervelus-generations-service':
        urlpatterns += [
            path('webhooks/generations/', include('generations.urls_webhooks'))
        ]