from rest_framework.routers import DefaultRouter
from .views import ColoniaViewSet

router = DefaultRouter()
router.register("colonias", ColoniaViewSet, basename="colonia")

urlpatterns = router.urls
