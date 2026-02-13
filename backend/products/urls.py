from django.urls import path
from . import views


urlpatterns = [
    path('store/', views.store, name='store'),
    path('styles/', views.style_list, name='style-list')
]