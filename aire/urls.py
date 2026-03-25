from rest_framework.routers import DefaultRouter

from .views import EstacionViewSet, LecturaViewSet

router = DefaultRouter()
router.register("estaciones", EstacionViewSet, basename="aire-estacion")
router.register("lecturas", LecturaViewSet, basename="aire-lectura")

urlpatterns = router.urls
