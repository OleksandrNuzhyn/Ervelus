from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from debug_toolbar.toolbar import debug_toolbar_urls


urlpatterns = []

if settings.DEBUG:
    urlpatterns += [
        path('admin/', admin.site.urls),

        path('webhooks/subscriptions/', include('subscriptions.urls_paddle_webhooks')),
        path('webhooks/subscriptions/', include('subscriptions.urls_tasks_webhooks')),
        path('webhooks/generations/', include('generations.urls_webhooks')),

        path('api/auth/', include('users.urls')),
        path('api/subscriptions/', include('subscriptions.urls_api')),
        path('api/products/', include('products.urls')),
        path('api/generations/', include('generations.urls_api')),
    ] + debug_toolbar_urls()
else:
    if settings.SERVICE_NAME == 'web_service':
        urlpatterns += [
            path('admin/', admin.site.urls),

            path('webhooks/subscriptions/', include('subscriptions.urls_paddle_webhooks')),

            path('api/auth/', include('users.urls')),
            path('api/subscriptions/', include('subscriptions.urls_api')),
            path('api/products/', include('products.urls')),
            path('api/generations/', include('generations.urls_api'))
        ]
    elif settings.SERVICE_NAME == 'generations_worker':
        urlpatterns += [
            path('webhooks/generations/', include('generations.urls_webhooks'))
        ]
    elif settings.SERVICE_NAME == 'subscriptions_worker':
        urlpatterns += [
            path('webhooks/subscriptions/', include('subscriptions.urls_tasks_webhooks'))
        ]