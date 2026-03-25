from django_filters.rest_framework import DjangoFilterBackend
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
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["cve_dleg", "cvegeo"]
    search_fields = ["nombre", "clave", "cvegeo"]
    ordering_fields = ["nombre", "cve_dleg", "updated_at"]
