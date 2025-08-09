from django.urls import path
from .views import GenerationRequestViewSet


urlpatterns = [
    path('generation-requests/', GenerationRequestViewSet.as_view({'get': 'list', 'post': 'create'}), name='generation-request-list-create'),
    path('generation-requests/latest/', GenerationRequestViewSet.as_view({'get': 'latest'}), name='generation-request-latest'),
]