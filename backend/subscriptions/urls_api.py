from django.urls import path
from .views import customer_portal_session_create


urlpatterns = [
    path('customer-portal/', customer_portal_session_create, name='customer-portal-create'),
]