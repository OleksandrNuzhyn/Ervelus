from django.urls import path
from . import views


urlpatterns = [
    path('subscription-plans/', views.subscription_plan_list, name='subscription-plan-list'),
    path('styles/', views.available_style_list, name='available-style-list')
]