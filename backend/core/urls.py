from django.contrib import admin
from django.urls import path, include
from core.auth_views import ConfirmEmailRedirectView

urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/auth/', include('dj_rest_auth.urls')),
    path('api/auth/registration/account-confirm-email/<str:key>/', ConfirmEmailRedirectView.as_view(), name='account_confirm_email'),
    path('api/auth/registration/', include('dj_rest_auth.registration.urls')),
]
