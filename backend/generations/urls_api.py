from rest_framework.routers import DefaultRouter
from .views import GenerationRequestViewSet

router = DefaultRouter()
router.register(r'generation-requests', GenerationRequestViewSet, basename='generation-request')


urlpatterns = router.urls