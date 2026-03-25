from rest_framework.routers import DefaultRouter
from .views import CarpetaInvestigacionViewSet

router = DefaultRouter()
router.register("carpetas", CarpetaInvestigacionViewSet, basename="carpeta")

urlpatterns = router.urls
