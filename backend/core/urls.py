from django.contrib import admin
from django.urls import path, include
from users.views import ConfirmEmailRedirectView, GoogleLogin


urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/auth/google/', GoogleLogin.as_view(), name='google_login'),
    path('api/auth/', include('dj_rest_auth.urls')),
    path('api/auth/registration/account-confirm-email/<str:key>/', ConfirmEmailRedirectView.as_view(), name='account_confirm_email'),
    path('api/auth/registration/', include('dj_rest_auth.registration.urls')),
]