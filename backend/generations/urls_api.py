from django.urls import path
from .views import GenerationRequestViewSet


urlpatterns = [
    path('generation-requests/', GenerationRequestViewSet.as_view({'post': 'create'}), name='generation-request-create'),
    path('generation-requests/latest/', GenerationRequestViewSet.as_view({'get': 'latest'}), name='generation-request-latest'),
    path('generation-requests/gallery/', GenerationRequestViewSet.as_view({'get': 'list'}), name='generation-request-gallery')
]