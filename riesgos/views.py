from rest_framework import viewsets
from rest_framework.filters import OrderingFilter, SearchFilter

from .models import RiesgoInundacion, Refugio
from .serializers import RiesgoInundacionSerializer, RefugioSerializer


class RiesgoInundacionViewSet(viewsets.ReadOnlyModelViewSet):
    """Atlas de riesgo de inundación. Filtros: ?alcaldia=Xochimilco, ?intensidad=Alto"""
    queryset = RiesgoInundacion.objects.all()
    serializer_class = RiesgoInundacionSerializer
    filter_backends = [OrderingFilter]
    ordering_fields = ["alcaldia", "intensidad", "area_m2"]

    def get_queryset(self):
        qs = super().get_queryset()
        for field in ("alcaldia", "intensidad", "r_p_v_e"):
            val = self.request.query_params.get(field)
            if val:
                qs = qs.filter(**{field: val})
        return qs


class RefugioViewSet(viewsets.ReadOnlyModelViewSet):
    """Refugios temporales CDMX. Filtros: ?delegacion=Cuauhtémoc"""
    queryset = Refugio.objects.all()
    serializer_class = RefugioSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ["nombre", "colonia"]
    ordering_fields = ["delegacion", "nombre", "cap_albergue"]

    def get_queryset(self):
        qs = super().get_queryset()
        val = self.request.query_params.get("delegacion")
        if val:
            qs = qs.filter(delegacion=val)
        return qs
