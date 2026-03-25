from rest_framework import viewsets
from rest_framework.filters import OrderingFilter, SearchFilter

from .models import CarpetaInvestigacion
from .serializers import CarpetaInvestigacionSerializer


class CarpetaInvestigacionViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Carpetas de investigación FGJ CDMX.
    Filtros: ?alcaldia_hechos=CUAUHTÉMOC, ?categoria_delito=..., ?anio=2018
    Búsqueda: ?search=lesiones
    """
    queryset = CarpetaInvestigacion.objects.all()
    serializer_class = CarpetaInvestigacionSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ["delito", "categoria_delito", "colonia_datos"]
    ordering_fields = ["fecha_hecho", "alcaldia_hechos", "categoria_delito"]

    def get_queryset(self):
        qs = super().get_queryset()
        for field in ("alcaldia_hechos", "categoria_delito", "ao_hechos"):
            val = self.request.query_params.get(field)
            if val:
                qs = qs.filter(**{field: val})
        return qs
