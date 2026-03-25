from rest_framework import serializers
from .models import RiesgoInundacion, Refugio


class RiesgoInundacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = RiesgoInundacion
        fields = [
            "id", "ckan_id", "fenomeno", "taxonomia", "r_p_v_e",
            "intensidad", "descripcion", "alcaldia", "cvegeo",
            "area_m2", "period_ret", "intens_num", "lat", "lon", "updated_at",
        ]


class RefugioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Refugio
        fields = [
            "id", "ckan_id", "nombre", "delegacion", "colonia",
            "calle_y_numero", "cp", "uso_inmueble", "cap_albergue",
            "region", "lat", "lon", "updated_at",
        ]
