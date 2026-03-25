from rest_framework import serializers

from .models import CicloEstacion, ViajesDiarios, ViajesDesglosados


class CicloEstacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CicloEstacion
        fields = [
            "id", "ckan_id", "sistema", "num_cicloe", "calle_prin", "calle_secu",
            "colonia", "alcaldia", "latitud", "longitud", "sitio_de_e", "estatus",
            "updated_at",
        ]


class ViajesDiariosSerializer(serializers.ModelSerializer):
    class Meta:
        model = ViajesDiarios
        fields = [
            "id", "ckan_id", "anio", "mes", "fecha", "genero", "viajes", "updated_at",
        ]


class ViajesDesglosadosSerializer(serializers.ModelSerializer):
    class Meta:
        model = ViajesDesglosados
        fields = [
            "id", "ckan_id", "anio", "mes", "fecha_corte", "hora",
            "genero", "rango_edad", "viajes", "updated_at",
        ]
