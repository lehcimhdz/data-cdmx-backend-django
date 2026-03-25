from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.filters import OrderingFilter, SearchFilter

from .models import RiesgoInundacion, Refugio
from .serializers import RiesgoInundacionSerializer, RefugioSerializer


class RiesgoInundacionViewSet(viewsets.ReadOnlyModelViewSet):
    """Atlas de riesgo de inundación. Filtros: ?alcaldia=Xochimilco&intensidad=Alto&r_p_v_e=Peligro"""
    queryset = RiesgoInundacion.objects.all()
    serializer_class = RiesgoInundacionSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["alcaldia", "intensidad", "r_p_v_e", "fenomeno"]
    search_fields = ["alcaldia", "descripcion"]
    ordering_fields = ["alcaldia", "intensidad", "area_m2"]


class RefugioViewSet(viewsets.ReadOnlyModelViewSet):
    """Refugios temporales CDMX. Filtros: ?delegacion=Cuauhtémoc&region=I"""
    queryset = Refugio.objects.all()
    serializer_class = RefugioSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["delegacion", "region"]
    search_fields = ["nombre", "colonia"]
    ordering_fields = ["delegacion", "nombre", "cap_albergue"]
