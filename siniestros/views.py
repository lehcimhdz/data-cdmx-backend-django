from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.filters import OrderingFilter, SearchFilter

from .models import SiniestroVial
from .serializers import SiniestroVialSerializer


class SiniestroVialViewSet(viewsets.ReadOnlyModelViewSet):
    """Siniestros viales SSC. Filtros: ?alcaldia=Cuauhtémoc&tipo_evento=Colisión"""
    queryset = SiniestroVial.objects.all()
    serializer_class = SiniestroVialSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["alcaldia", "tipo_evento"]
    search_fields = ["colonia"]
    ordering_fields = ["fecha", "alcaldia", "fallecidos", "lesionados"]
