from django.contrib import admin
from .models import AfluenciaMetro, AfluenciaMetrobus, AfluenciaSTE, AfluenciaRTP


@admin.register(AfluenciaMetro)
class AfluenciaMetroAdmin(admin.ModelAdmin):
    list_display = ["linea", "estacion", "fecha", "source", "tipo_pago", "afluencia"]
    list_filter = ["source", "linea", "anio"]
    search_fields = ["linea", "estacion"]
    readonly_fields = ["ckan_id", "created_at", "updated_at"]


@admin.register(AfluenciaMetrobus)
class AfluenciaMetrobusAdmin(admin.ModelAdmin):
    list_display = ["linea", "fecha", "source", "tipo_pago", "afluencia"]
    list_filter = ["source", "linea", "anio"]
    search_fields = ["linea"]
    readonly_fields = ["ckan_id", "created_at", "updated_at"]


@admin.register(AfluenciaSTE)
class AfluenciaSTEAdmin(admin.ModelAdmin):
    list_display = ["sistema", "linea", "fecha", "tipo_pago", "afluencia"]
    list_filter = ["sistema", "anio"]
    readonly_fields = ["ckan_id", "created_at", "updated_at"]


@admin.register(AfluenciaRTP)
class AfluenciaRTPAdmin(admin.ModelAdmin):
    list_display = ["servicio", "fecha", "tipo_pago", "afluencia"]
    list_filter = ["anio", "servicio"]
    readonly_fields = ["ckan_id", "created_at", "updated_at"]
