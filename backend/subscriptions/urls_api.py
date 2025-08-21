from django.urls import path
from . import views


urlpatterns = [
    path('user-subscriptions/', views.user_subscription_list, name='user-subscription-list')
]