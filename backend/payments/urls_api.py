from django.urls import path
from . import views


urlpatterns = [
    path('create-star-invoice-link/', views.create_star_invoice_link, name='create-star-invoice-link'),
]