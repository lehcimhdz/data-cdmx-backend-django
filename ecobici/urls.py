from rest_framework.routers import DefaultRouter

from .views import CicloEstacionViewSet, ViajesDiariosViewSet, ViajesDesglosadosViewSet

router = DefaultRouter()
router.register("estaciones", CicloEstacionViewSet, basename="cicloestacion")
router.register("viajes-diarios", ViajesDiariosViewSet, basename="viajesdiarios")
router.register("viajes-desglosados", ViajesDesglosadosViewSet, basename="viajesdesglosados")

urlpatterns = router.urls
