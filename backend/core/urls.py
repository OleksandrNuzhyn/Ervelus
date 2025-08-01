from django.contrib import admin
from django.urls import path, include
from django.conf import settings


urlpatterns = []

if settings.SERVICE_NAME == 'web_service':
    urlpatterns += [
        path('admin/', admin.site.urls),
        
        path('webhooks/subscriptions/', include('subscriptions.urls_webhooks')),

        path('api/auth/', include('users.urls')),
        path('api/subscriptions/', include('subscriptions.urls_api')),
        path('api/products/', include('products.urls')),
        path('api/generations/', include('generations.urls_api'))
    ]

elif settings.SERVICE_NAME == 'generations_worker':
    urlpatterns += [
        path('webhooks/generations/', include('generations.urls_webhooks')),
    ]