from rest_framework import serializers
from .models import AfluenciaMetro, AfluenciaMetrobus, AfluenciaSTE, AfluenciaRTP


class AfluenciaMetroSerializer(serializers.ModelSerializer):
    class Meta:
        model = AfluenciaMetro
        fields = ["id", "ckan_id", "source", "fecha", "anio", "mes",
                  "linea", "estacion", "tipo_pago", "afluencia", "updated_at"]


class AfluenciaMetrobusSerializer(serializers.ModelSerializer):
    class Meta:
        model = AfluenciaMetrobus
        fields = ["id", "ckan_id", "source", "fecha", "anio", "mes",
                  "linea", "tipo_pago", "afluencia", "updated_at"]


class AfluenciaSTESerializer(serializers.ModelSerializer):
    sistema_display = serializers.CharField(source="get_sistema_display", read_only=True)

    class Meta:
        model = AfluenciaSTE
        fields = ["id", "ckan_id", "sistema", "sistema_display", "fecha", "anio", "mes",
                  "linea", "tipo_pago", "afluencia", "updated_at"]


class AfluenciaRTPSerializer(serializers.ModelSerializer):
    class Meta:
        model = AfluenciaRTP
        fields = ["id", "ckan_id", "fecha", "anio", "mes",
                  "servicio", "tipo_pago", "afluencia", "updated_at"]
