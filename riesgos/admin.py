from django.contrib import admin
from .models import RiesgoInundacion, Refugio


@admin.register(RiesgoInundacion)
class RiesgoInundacionAdmin(admin.ModelAdmin):
    list_display = ["taxonomia", "intensidad", "alcaldia", "cvegeo", "period_ret", "area_m2"]
    list_filter = ["intensidad", "alcaldia", "r_p_v_e"]
    search_fields = ["alcaldia", "cvegeo", "descripcion"]
    readonly_fields = ["ckan_id", "created_at", "updated_at"]


@admin.register(Refugio)
class RefugioAdmin(admin.ModelAdmin):
    list_display = ["nombre", "delegacion", "colonia", "uso_inmueble", "cap_albergue", "region"]
    list_filter = ["delegacion", "region", "uso_inmueble"]
    search_fields = ["nombre", "colonia", "calle_y_numero"]
    readonly_fields = ["ckan_id", "created_at", "updated_at"]
