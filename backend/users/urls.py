from django.urls import path
from . import views


urlpatterns = [
    path('account/delete/', views.account_delete, name='account-delete'),
    path('credit-balance/', views.user_credit_balance, name='user-credit-balance')
]