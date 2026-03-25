from django.db import models


class Colonia(models.Model):
    """
    Catálogo de colonias de la Ciudad de México.

    Fuente: datos.cdmx.gob.mx
    Resource ID: 03368e1e-f05e-4bea-ac17-58fc650f6fee
    """

    # Identificadores originales del dataset
    ckan_id = models.IntegerField(unique=True, help_text="Campo _id de CKAN")
    gid = models.IntegerField(null=True, blank=True)
    object_id = models.IntegerField(null=True, blank=True)

    # Datos administrativos
    nombre = models.CharField(max_length=255)
    clave = models.CharField(max_length=50, blank=True)
    cvegeo = models.CharField(max_length=50, blank=True, help_text="Clave geográfica censal")
    cve_dleg = models.CharField(max_length=10, blank=True, help_text="Clave de alcaldía")

    # Límites electorales/administrativos
    coun_left = models.IntegerField(null=True, blank=True)
    coun_right = models.IntegerField(null=True, blank=True)

    # Coordenadas del centroide
    lat = models.FloatField(null=True, blank=True)
    lon = models.FloatField(null=True, blank=True)

    # Auditoría
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["nombre"]
        verbose_name = "Colonia"
        verbose_name_plural = "Colonias"

    def __str__(self) -> str:
        return f"{self.nombre} ({self.cve_dleg})"
