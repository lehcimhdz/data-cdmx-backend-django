from django.db import models


class RiesgoInundacion(models.Model):
    """
    Atlas de Riesgo — Inundaciones por AGEB.

    Fuente: resource_id=b6249921-7811-4a48-a82a-60fcec5e5184 (~4,908 registros)
    """

    ckan_id = models.IntegerField(unique=True)

    fenomeno = models.CharField(max_length=100, blank=True)
    taxonomia = models.CharField(max_length=100, blank=True)
    r_p_v_e = models.CharField(max_length=50, blank=True, help_text="Riesgo/Peligro/Vulnerabilidad/Exposición")
    intensidad = models.CharField(max_length=50, blank=True)
    descripcion = models.TextField(blank=True)
    fuente = models.CharField(max_length=255, blank=True)

    # Ubicación
    cvegeo = models.CharField(max_length=20, blank=True, help_text="Clave geográfica AGEB")
    alcaldia = models.CharField(max_length=100, blank=True)
    entidad = models.CharField(max_length=100, blank=True)
    lat = models.FloatField(null=True, blank=True)
    lon = models.FloatField(null=True, blank=True)

    # Métricas geométricas
    area_m2 = models.FloatField(null=True, blank=True)
    perime_m = models.FloatField(null=True, blank=True)

    # Atributos de riesgo
    period_ret = models.CharField(max_length=50, blank=True, help_text="Período de retorno")
    intens_uni = models.CharField(max_length=100, blank=True, help_text="Unidad de intensidad")
    intens_num = models.CharField(max_length=50, blank=True, help_text="Rango de intensidad")
    int2 = models.IntegerField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["alcaldia", "intensidad"]
        indexes = [
            models.Index(fields=["alcaldia"]),
            models.Index(fields=["intensidad"]),
            models.Index(fields=["cvegeo"]),
        ]
        verbose_name = "Riesgo de Inundación"
        verbose_name_plural = "Riesgos de Inundación"

    def __str__(self) -> str:
        return f"{self.taxonomia} – {self.intensidad} ({self.alcaldia})"


class Refugio(models.Model):
    """
    Refugios temporales de la CDMX para respuesta a desastres.

    Fuente: resource_id=96d69f40-004e-4525-ae6a-bb7421b482fd (~67 registros)
    """

    ckan_id = models.IntegerField(unique=True)

    nombre = models.CharField(max_length=255)
    delegacion = models.CharField(max_length=100, blank=True)
    colonia = models.CharField(max_length=255, blank=True)
    calle_y_numero = models.CharField(max_length=255, blank=True)
    cp = models.IntegerField(null=True, blank=True)
    uso_inmueble = models.CharField(max_length=100, blank=True)
    cap_albergue = models.IntegerField(null=True, blank=True, help_text="Capacidad de albergue en personas")
    region = models.CharField(max_length=50, blank=True)
    fuente = models.CharField(max_length=255, blank=True)
    lat = models.FloatField(null=True, blank=True)
    lon = models.FloatField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["delegacion", "nombre"]
        verbose_name = "Refugio Temporal"
        verbose_name_plural = "Refugios Temporales"

    def __str__(self) -> str:
        return f"{self.nombre} ({self.delegacion})"
