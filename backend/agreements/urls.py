from django.urls import path
from . import views


urlpatterns = [
    path('published/', views.published_agreements_list_view, name='published-list'),
    path('pending/', views.pending_agreements_list_view, name='pending-list'),
    path('accept_single/', views.accept_agreement, name='accept_single'),
]