from django.contrib import admin

from .models import SiniestroVial


@admin.register(SiniestroVial)
class SiniestroVialAdmin(admin.ModelAdmin):
    list_display = ["fecha", "tipo_evento", "alcaldia", "colonia", "lesionados", "fallecidos"]
    list_filter = ["alcaldia", "tipo_evento"]
    search_fields = ["colonia"]
    date_hierarchy = "fecha"
