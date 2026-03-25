from rest_framework import viewsets
from rest_framework.filters import OrderingFilter, SearchFilter

from .models import Colonia
from .serializers import ColoniaSerializer


class ColoniaViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API de colonias de la CDMX.

    Soporta búsqueda por nombre (`?search=tepito`) y
    filtrado por alcaldía (`?cve_dleg=06`).
    """

    queryset = Colonia.objects.all()
    serializer_class = ColoniaSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ["nombre", "clave", "cvegeo"]
    ordering_fields = ["nombre", "cve_dleg", "updated_at"]

    def get_queryset(self):
        qs = super().get_queryset()
        cve_dleg = self.request.query_params.get("cve_dleg")
        if cve_dleg:
            qs = qs.filter(cve_dleg=cve_dleg)
        return qs
