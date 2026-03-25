from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.filters import OrderingFilter, SearchFilter

from .models import CarpetaInvestigacion
from .serializers import CarpetaInvestigacionSerializer


class CarpetaInvestigacionViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Carpetas de investigación FGJ CDMX.
    Filtros: ?alcaldia_hechos=CUAUHTÉMOC&categoria_delito=DELITO+DE+ALTO+IMPACTO&ao_hechos=2018
    Búsqueda: ?search=lesiones
    """
    queryset = CarpetaInvestigacion.objects.all()
    serializer_class = CarpetaInvestigacionSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["alcaldia_hechos", "categoria_delito", "ao_hechos", "mes_hechos"]
    search_fields = ["delito", "categoria_delito", "colonia_datos"]
    ordering_fields = ["fecha_hecho", "alcaldia_hechos", "categoria_delito"]
