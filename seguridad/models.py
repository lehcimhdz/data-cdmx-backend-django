from django.db import models


class CarpetaInvestigacion(models.Model):
    """
    Carpetas de investigación de la Fiscalía General de Justicia (FGJ) CDMX.

    Fuente: resource_id=3f308147-b1fc-49a9-92b7-e74f3f79aa9c (~808 K registros)
    Cobertura: enero 2016 – junio 2019.
    """

    ckan_id = models.IntegerField(unique=True)

    # Datos del hecho
    ao_hechos = models.CharField(max_length=10, blank=True)
    mes_hechos = models.CharField(max_length=20, blank=True)
    fecha_hecho = models.DateField(null=True, blank=True)
    hora_hecho = models.CharField(max_length=10, blank=True)

    # Datos de inicio de carpeta
    ao_inicio = models.IntegerField(null=True, blank=True)
    mes_inicio = models.CharField(max_length=20, blank=True)
    fecha_inicio = models.DateField(null=True, blank=True)
    hora_inicio = models.CharField(max_length=10, blank=True)

    # Clasificación del delito
    delito = models.CharField(max_length=255)
    categoria_delito = models.CharField(max_length=100, blank=True)
    fiscalia = models.CharField(max_length=255, blank=True)
    agencia = models.CharField(max_length=100, blank=True)
    unidad_investigacion = models.CharField(max_length=100, blank=True)

    # Ubicación
    alcaldia_hechos = models.CharField(max_length=100, blank=True)
    municipio_hechos = models.CharField(max_length=100, blank=True)
    colonia_datos = models.CharField(max_length=255, blank=True)
    fgj_colonia_registro = models.CharField(max_length=255, blank=True)
    longitud = models.FloatField(null=True, blank=True)
    latitud = models.FloatField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-fecha_hecho"]
        indexes = [
            models.Index(fields=["categoria_delito"]),
            models.Index(fields=["alcaldia_hechos"]),
            models.Index(fields=["fecha_hecho"]),
        ]
        verbose_name = "Carpeta de Investigación"
        verbose_name_plural = "Carpetas de Investigación"

    def __str__(self) -> str:
        return f"{self.delito} – {self.alcaldia_hechos} ({self.fecha_hecho})"
