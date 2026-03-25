from django.contrib import admin

from .models import CicloEstacion, ViajesDiarios, ViajesDesglosados


@admin.register(CicloEstacion)
class CicloEstacionAdmin(admin.ModelAdmin):
    list_display = ["num_cicloe", "calle_prin", "alcaldia", "estatus"]
    list_filter = ["alcaldia", "estatus", "sistema"]
    search_fields = ["num_cicloe", "calle_prin", "calle_secu", "colonia"]


@admin.register(ViajesDiarios)
class ViajesDiariosAdmin(admin.ModelAdmin):
    list_display = ["fecha", "genero", "viajes"]
    list_filter = ["genero", "anio", "mes"]


@admin.register(ViajesDesglosados)
class ViajesDesglosadosAdmin(admin.ModelAdmin):
    list_display = ["fecha_corte", "hora", "genero", "rango_edad", "viajes"]
    list_filter = ["genero", "rango_edad", "anio", "mes"]
