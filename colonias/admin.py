from django.contrib import admin
from .models import Colonia


@admin.register(Colonia)
class ColoniaAdmin(admin.ModelAdmin):
    list_display = ["nombre", "clave", "cve_dleg", "cvegeo", "lat", "lon", "updated_at"]
    list_filter = ["cve_dleg"]
    search_fields = ["nombre", "clave", "cvegeo"]
    readonly_fields = ["ckan_id", "created_at", "updated_at"]
