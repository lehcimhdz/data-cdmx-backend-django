from rest_framework import serializers

from .models import Estacion, Lectura


class EstacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Estacion
        fields = [
            "id", "ckan_id", "id_estacion", "nombre", "alcaldia",
            "latitud", "longitud", "updated_at",
        ]


class LecturaSerializer(serializers.ModelSerializer):
    estacion_id_estacion = serializers.CharField(source="estacion.id_estacion", read_only=True, default=None)

    class Meta:
        model = Lectura
        fields = [
            "id", "ckan_id", "estacion", "estacion_id_estacion",
            "contaminante", "valor", "unidad", "fecha", "hora", "updated_at",
        ]
