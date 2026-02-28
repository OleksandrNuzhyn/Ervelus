from django.urls import path
from . import views


urlpatterns = [
    path('auth/', views.telegram_auth, name='telegram-auth'),
    path('share-invite/', views.share_invite, name='share-invite'),
    path('share-generation/', views.share_generation, name='share-generation')
]