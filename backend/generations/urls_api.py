from django.urls import path
from .views import GenerationRequestViewSet


urlpatterns = [
    path('generation-requests/create/', GenerationRequestViewSet.as_view({'post': 'create'}), name='generation-request-create'),
    path('generation-requests/latest/', GenerationRequestViewSet.as_view({'get': 'latest'}), name='generation-request-latest'),
    path('generation-requests/gallery/', GenerationRequestViewSet.as_view({'get': 'list'}), name='generation-request-gallery'),
    path('generation-requests/retrieve/<int:pk>/', GenerationRequestViewSet.as_view({'get': 'retrieve'}), name='generation-request-retrieve'),
    path('generation-requests/delete/<int:pk>/', GenerationRequestViewSet.as_view({'delete': 'destroy'}), name='generation-request-delete'),
    path('generation-requests/stop/<int:pk>/', GenerationRequestViewSet.as_view({'post': 'stop'}), name='generation-request-stop')
]