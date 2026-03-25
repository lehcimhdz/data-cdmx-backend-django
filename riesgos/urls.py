from rest_framework.routers import DefaultRouter
from .views import RiesgoInundacionViewSet, RefugioViewSet

router = DefaultRouter()
router.register("inundaciones", RiesgoInundacionViewSet, basename="inundacion")
router.register("refugios", RefugioViewSet, basename="refugio")

urlpatterns = router.urls
