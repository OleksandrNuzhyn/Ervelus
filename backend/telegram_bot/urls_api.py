from django.urls import path
from . import views


urlpatterns = [
    path('auth/', views.telegram_auth, name='telegram-auth'),
    path('prepare-invite/', views.prepare_invite, name='prepare-invite'),
    path('prepare-share/<int:pk>/', views.prepare_share, name='prepare-share')
]