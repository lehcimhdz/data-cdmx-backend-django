from rest_framework import serializers

from .models import SiniestroVial


class SiniestroVialSerializer(serializers.ModelSerializer):
    class Meta:
        model = SiniestroVial
        fields = [
            "id", "ckan_id", "fecha", "tipo_evento", "alcaldia", "colonia",
            "latitud", "longitud", "vehiculos_involucrados", "lesionados",
            "fallecidos", "updated_at",
        ]
