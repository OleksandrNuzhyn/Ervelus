from django.contrib import admin
from django.urls import path, include
from dj_rest_auth.views import PasswordResetConfirmView
from users.views import GoogleLogin, get_csrf_token


urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/get-csrf-token/', get_csrf_token, name='get-csrf-token'),
    
    path('api/auth/password/reset/confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('api/auth/google/', GoogleLogin.as_view(), name='google_login'),
    path('api/auth/', include('dj_rest_auth.urls')),
    path('api/auth/registration/', include('dj_rest_auth.registration.urls')),
]