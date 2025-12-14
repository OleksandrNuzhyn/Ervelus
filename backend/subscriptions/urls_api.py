from django.urls import path
from . import views


urlpatterns = [
    path('create-order/', views.create_order, name='create-order'),
    path('user-subscriptions/', views.user_subscription_list, name='user-subscription-list'),
    path('cancel-subscription/<int:id>/', views.cancel_subscription, name='cancel-subscription')
]