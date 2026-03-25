from rest_framework.routers import DefaultRouter
from .views import AfluenciaMetroViewSet, AfluenciaMetrobusViewSet, AfluenciaSTEViewSet, AfluenciaRTPViewSet

router = DefaultRouter()
router.register("metro", AfluenciaMetroViewSet, basename="metro")
router.register("metrobus", AfluenciaMetrobusViewSet, basename="metrobus")
router.register("ste", AfluenciaSTEViewSet, basename="ste")
router.register("rtp", AfluenciaRTPViewSet, basename="rtp")

urlpatterns = router.urls
