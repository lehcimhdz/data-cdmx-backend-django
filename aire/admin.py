from django.contrib import admin

from .models import Estacion, Lectura


@admin.register(Estacion)
class EstacionAdmin(admin.ModelAdmin):
    list_display = ["id_estacion", "nombre", "alcaldia", "latitud", "longitud"]
    list_filter = ["alcaldia"]
    search_fields = ["id_estacion", "nombre"]


@admin.register(Lectura)
class LecturaAdmin(admin.ModelAdmin):
    list_display = ["estacion", "contaminante", "valor", "unidad", "fecha", "hora"]
    list_filter = ["contaminante", "estacion"]
    raw_id_fields = ["estacion"]
