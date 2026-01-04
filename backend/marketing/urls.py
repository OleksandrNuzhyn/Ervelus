from django.urls import path
from . import views


urlpatterns = [
    path('promo-codes/', views.apply_promo_code, name='apply-promo-code'),
]