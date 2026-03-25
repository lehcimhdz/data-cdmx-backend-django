from django.db import models


class SiniestroVial(models.Model):
    """
    Siniestros viales reportados por la SSC (Secretaría de Seguridad Ciudadana).

    Fuente: datos.cdmx.gob.mx — SSC siniestros viales
    Campos API: _id, fecha, tipo_evento, alcaldia, colonia, latitud, longitud,
                vehiculos_involucrados, lesionados, fallecidos
    """

    ckan_id = models.IntegerField(unique=True)

    fecha = models.DateField(null=True, blank=True)
    tipo_evento = models.CharField(max_length=100, blank=True,
                                   help_text="Colisión, atropellamiento, volcadura…")
    alcaldia = models.CharField(max_length=100, blank=True)
    colonia = models.CharField(max_length=255, blank=True)
    latitud = models.FloatField(null=True, blank=True)
    longitud = models.FloatField(null=True, blank=True)
    vehiculos_involucrados = models.IntegerField(null=True, blank=True)
    lesionados = models.IntegerField(null=True, blank=True)
    fallecidos = models.IntegerField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-fecha", "alcaldia"]
        indexes = [
            models.Index(fields=["alcaldia", "fecha", "tipo_evento"]),
            models.Index(fields=["fecha"]),
        ]
        verbose_name = "Siniestro Vial"
        verbose_name_plural = "Siniestros Viales"

    def __str__(self) -> str:
        return f"{self.tipo_evento} – {self.alcaldia} ({self.fecha})"
