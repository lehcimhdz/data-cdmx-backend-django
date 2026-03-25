from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.filters import OrderingFilter, SearchFilter

from .models import AfluenciaMetro, AfluenciaMetrobus, AfluenciaSTE, AfluenciaRTP
from .serializers import (
    AfluenciaMetroSerializer,
    AfluenciaMetrobusSerializer,
    AfluenciaSTESerializer,
    AfluenciaRTPSerializer,
)


class AfluenciaMetroViewSet(viewsets.ReadOnlyModelViewSet):
    """Afluencia Metro CDMX. Filtros: ?linea=Linea+1&anio=2023&source=simple"""
    queryset = AfluenciaMetro.objects.all()
    serializer_class = AfluenciaMetroSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["linea", "estacion", "source", "anio", "mes"]
    search_fields = ["linea", "estacion"]
    ordering_fields = ["fecha", "linea", "estacion", "afluencia"]


class AfluenciaMetrobusViewSet(viewsets.ReadOnlyModelViewSet):
    """Afluencia Metrobús CDMX. Filtros: ?linea=Línea+1&source=simple&anio=2022"""
    queryset = AfluenciaMetrobus.objects.all()
    serializer_class = AfluenciaMetrobusSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["linea", "source", "anio", "mes"]
    search_fields = ["linea"]
    ordering_fields = ["fecha", "linea", "afluencia"]


class AfluenciaSTEViewSet(viewsets.ReadOnlyModelViewSet):
    """Afluencia STE (Tren Ligero, Cablebus, Trolebús). Filtros: ?sistema=cablebus&anio=2023"""
    queryset = AfluenciaSTE.objects.all()
    serializer_class = AfluenciaSTESerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ["sistema", "linea", "anio", "mes"]
    ordering_fields = ["fecha", "sistema", "afluencia"]


class AfluenciaRTPViewSet(viewsets.ReadOnlyModelViewSet):
    """Afluencia RTP. Filtros: ?servicio=Ordinario&anio=2023"""
    queryset = AfluenciaRTP.objects.all()
    serializer_class = AfluenciaRTPSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["servicio", "anio", "mes"]
    search_fields = ["servicio"]
    ordering_fields = ["fecha", "servicio", "afluencia"]
