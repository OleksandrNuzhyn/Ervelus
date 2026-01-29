from django.urls import path
from . import views


urlpatterns = [
    path('star-packages/', views.star_package_list, name='star-package-list'),
    path('styles/', views.available_style_list, name='available-style-list')
]