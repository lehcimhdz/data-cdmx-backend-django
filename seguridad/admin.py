from django.contrib import admin
from .models import CarpetaInvestigacion


@admin.register(CarpetaInvestigacion)
class CarpetaInvestigacionAdmin(admin.ModelAdmin):
    list_display = ["delito", "categoria_delito", "alcaldia_hechos", "fecha_hecho", "ao_hechos"]
    list_filter = ["categoria_delito", "alcaldia_hechos", "ao_hechos"]
    search_fields = ["delito", "colonia_datos", "fiscalia"]
    readonly_fields = ["ckan_id", "created_at", "updated_at"]
