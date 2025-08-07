from adrf.routers import DefaultRouter
from .views import GenerationRequestViewSet

router = DefaultRouter()
router.register(r'generation-requests', GenerationRequestViewSet, basename='generation-request')


urlpatterns = router.urls