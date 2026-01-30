from django.urls import path, include
from .views import GoogleLogin, CustomVerifyEmailView
from dj_rest_auth.views import PasswordResetConfirmView
from . import views


urlpatterns = [
    path('account/delete/', views.account_delete, name='account-delete'),
    path('credit-balance/', views.user_credit_balance, name='user-credit-balance'),
    path('password/reset/confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('google/', GoogleLogin.as_view(), name='google-login'),
    path('', include('dj_rest_auth.urls')),
    path('registration/verify-email/', CustomVerifyEmailView.as_view(), name='account_confirm_email'),
    path('registration/', include('dj_rest_auth.registration.urls'))
]