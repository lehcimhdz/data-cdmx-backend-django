from rest_framework.routers import DefaultRouter

from .views import SiniestroVialViewSet

router = DefaultRouter()
router.register("", SiniestroVialViewSet, basename="siniestrovial")

urlpatterns = router.urls
