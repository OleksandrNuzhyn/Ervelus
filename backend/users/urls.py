from django.urls import path
from . import views


urlpatterns = [
    path('delete-account/', views.delete_account, name='delete-account'),
    path('credit-balance/', views.credit_balance, name='credit-balance')
]