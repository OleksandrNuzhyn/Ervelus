from django.contrib import admin
from django.urls import path, include
from users.views import ConfirmEmailRedirectView, PasswordResetRedirectView

urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/auth/password/reset/confirm/<uidb64>/<token>/', PasswordResetRedirectView.as_view(), name='password_reset_confirm'),
    path('api/auth/', include('dj_rest_auth.urls')),
    path('api/auth/registration/account-confirm-email/<str:key>/', ConfirmEmailRedirectView.as_view(), name='account_confirm_email'),
    path('api/auth/registration/', include('dj_rest_auth.registration.urls')),
]
