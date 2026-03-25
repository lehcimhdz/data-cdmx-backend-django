from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.filters import OrderingFilter, SearchFilter

from .models import CicloEstacion, ViajesDiarios, ViajesDesglosados
from .serializers import CicloEstacionSerializer, ViajesDiariosSerializer, ViajesDesglosadosSerializer


class CicloEstacionViewSet(viewsets.ReadOnlyModelViewSet):
    """Estaciones ECOBICI. Filtros: ?alcaldia=Cuauhtémoc&estatus=AC"""
    queryset = CicloEstacion.objects.all()
    serializer_class = CicloEstacionSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["alcaldia", "estatus", "sistema"]
    search_fields = ["calle_prin", "calle_secu", "colonia", "num_cicloe"]
    ordering_fields = ["alcaldia", "num_cicloe"]


class ViajesDiariosViewSet(viewsets.ReadOnlyModelViewSet):
    """Viajes diarios ECOBICI. Filtros: ?anio=2024&mes=3&genero=M"""
    queryset = ViajesDiarios.objects.all()
    serializer_class = ViajesDiariosSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ["anio", "mes", "genero"]
    ordering_fields = ["fecha", "viajes"]


class ViajesDesglosadosViewSet(viewsets.ReadOnlyModelViewSet):
    """Viajes ECOBICI por hora, género y edad. Filtros: ?anio=2024&mes=3&genero=M&rango_edad=26-35"""
    queryset = ViajesDesglosados.objects.all()
    serializer_class = ViajesDesglosadosSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ["anio", "mes", "genero", "rango_edad"]
    ordering_fields = ["fecha_corte", "hora", "viajes"]
