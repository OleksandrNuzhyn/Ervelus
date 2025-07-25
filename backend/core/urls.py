from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('webhooks/', include('subscriptions.urls_webhooks')),

    path('api/auth/', include('users.urls')),
    path('api/subscriptions/', include('subscriptions.urls_api')),
    path('api/products/', include('products.urls')),
]