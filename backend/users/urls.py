from django.urls import path, include
from .views import GoogleLogin
from . import views
from dj_rest_auth.views import PasswordResetConfirmView


urlpatterns = [
    path('csrf-token/', views.csrf_token, name='csrf-token'),
    path('account/delete/', views.account_delete, name='account-delete'),
    path('credit-balance/', views.user_credit_balance, name='user-credit-balance'),
    path('password/reset/confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('google/', GoogleLogin.as_view(), name='google_login'),
    path('', include('dj_rest_auth.urls')),
    path('registration/', include('dj_rest_auth.registration.urls'))
]