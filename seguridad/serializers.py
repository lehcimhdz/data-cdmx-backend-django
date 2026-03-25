from rest_framework import serializers
from .models import CarpetaInvestigacion


class CarpetaInvestigacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarpetaInvestigacion
        fields = [
            "id", "ckan_id", "fecha_hecho", "ao_hechos", "mes_hechos",
            "delito", "categoria_delito", "competencia", "fiscalia", "agencia",
            "alcaldia_hechos", "alcaldia_catalogo", "colonia_datos",
            "latitud", "longitud", "updated_at",
        ]
