from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.filters import OrderingFilter, SearchFilter

from .models import Estacion, Lectura
from .serializers import EstacionSerializer, LecturaSerializer


class EstacionViewSet(viewsets.ReadOnlyModelViewSet):
    """Estaciones de monitoreo de aire SEDEMA/SIMAT. Filtros: ?alcaldia=Iztapalapa"""
    queryset = Estacion.objects.all()
    serializer_class = EstacionSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["alcaldia"]
    search_fields = ["nombre", "id_estacion"]
    ordering_fields = ["alcaldia", "nombre"]


class LecturaViewSet(viewsets.ReadOnlyModelViewSet):
    """Lecturas de calidad del aire. Filtros: ?estacion=1&contaminante=PM2.5&fecha=2024-03-01"""
    queryset = Lectura.objects.select_related("estacion").all()
    serializer_class = LecturaSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ["estacion", "contaminante", "fecha"]
    ordering_fields = ["fecha", "hora", "valor"]
