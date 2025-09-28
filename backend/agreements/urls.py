from django.urls import path
from . import views


urlpatterns = [
    path('accept_user_document_version/', views.accept_user_document_version_client_side, name='accept_user_document_version'),
    path('<str:document_type>/', views.latest_document_version_detail, name='detail')
]