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
    """Afluencia Metro CDMX. Filtros: ?linea=Linea+1, ?estacion=Zaragoza, ?source=simple"""
    queryset = AfluenciaMetro.objects.all()
    serializer_class = AfluenciaMetroSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ["linea", "estacion"]
    ordering_fields = ["fecha", "linea", "estacion", "afluencia"]

    def get_queryset(self):
        qs = super().get_queryset()
        for field in ("linea", "estacion", "source", "anio"):
            val = self.request.query_params.get(field)
            if val:
                qs = qs.filter(**{field: val})
        return qs


class AfluenciaMetrobusViewSet(viewsets.ReadOnlyModelViewSet):
    """Afluencia Metrobús CDMX. Filtros: ?linea=Línea+1, ?source=simple"""
    queryset = AfluenciaMetrobus.objects.all()
    serializer_class = AfluenciaMetrobusSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ["linea"]
    ordering_fields = ["fecha", "linea", "afluencia"]

    def get_queryset(self):
        qs = super().get_queryset()
        for field in ("linea", "source", "anio"):
            val = self.request.query_params.get(field)
            if val:
                qs = qs.filter(**{field: val})
        return qs


class AfluenciaSTEViewSet(viewsets.ReadOnlyModelViewSet):
    """Afluencia STE (Tren Ligero, Cablebus, Trolebús). Filtros: ?sistema=cablebus"""
    queryset = AfluenciaSTE.objects.all()
    serializer_class = AfluenciaSTESerializer
    filter_backends = [OrderingFilter]
    ordering_fields = ["fecha", "sistema", "afluencia"]

    def get_queryset(self):
        qs = super().get_queryset()
        for field in ("sistema", "linea", "anio"):
            val = self.request.query_params.get(field)
            if val:
                qs = qs.filter(**{field: val})
        return qs


class AfluenciaRTPViewSet(viewsets.ReadOnlyModelViewSet):
    """Afluencia RTP. Filtros: ?servicio=..."""
    queryset = AfluenciaRTP.objects.all()
    serializer_class = AfluenciaRTPSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ["servicio"]
    ordering_fields = ["fecha", "servicio", "afluencia"]

    def get_queryset(self):
        qs = super().get_queryset()
        for field in ("servicio", "anio"):
            val = self.request.query_params.get(field)
            if val:
                qs = qs.filter(**{field: val})
        return qs
