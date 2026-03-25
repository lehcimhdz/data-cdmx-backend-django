from django.db import models


class Estacion(models.Model):
    """
    Estaciones de monitoreo de calidad del aire SEDEMA / SIMAT.

    Fuente: datos.cdmx.gob.mx — red de monitoreo atmosférico
    Campos API: _id, id_estacion, nombre, alcaldia, latitud, longitud
    """

    ckan_id = models.IntegerField(unique=True)

    id_estacion = models.CharField(max_length=20, unique=True, help_text="Clave corta, e.g. BJU, MER")
    nombre = models.CharField(max_length=255, blank=True)
    alcaldia = models.CharField(max_length=100, blank=True)
    latitud = models.FloatField(null=True, blank=True)
    longitud = models.FloatField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["alcaldia", "nombre"]
        indexes = [
            models.Index(fields=["alcaldia"]),
        ]
        verbose_name = "Estación de Monitoreo"
        verbose_name_plural = "Estaciones de Monitoreo"

    def __str__(self) -> str:
        return f"{self.id_estacion} – {self.nombre} ({self.alcaldia})"


class Lectura(models.Model):
    """
    Lecturas horarias de calidad del aire por estación y contaminante.

    Fuente: datos.cdmx.gob.mx — SIMAT SEDEMA
    Campos API: _id, id_estacion, contaminante, valor, unidad, fecha, hora
    Índice compuesto: (estacion, contaminante, fecha)
    """

    ckan_id = models.IntegerField(unique=True)

    estacion = models.ForeignKey(
        Estacion,
        on_delete=models.CASCADE,
        related_name="lecturas",
        null=True,
        blank=True,
    )
    contaminante = models.CharField(max_length=20, blank=True, help_text="PM2.5, O3, CO, NO2, SO2…")
    valor = models.FloatField(null=True, blank=True)
    unidad = models.CharField(max_length=50, blank=True)
    fecha = models.DateField(null=True, blank=True)
    hora = models.IntegerField(null=True, blank=True, help_text="Hora del día (0–23)")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-fecha", "hora", "contaminante"]
        indexes = [
            models.Index(fields=["estacion", "contaminante", "fecha"]),
            models.Index(fields=["contaminante"]),
            models.Index(fields=["fecha"]),
        ]
        verbose_name = "Lectura de Calidad del Aire"
        verbose_name_plural = "Lecturas de Calidad del Aire"

    def __str__(self) -> str:
        estacion_str = self.estacion.id_estacion if self.estacion_id else "?"
        return f"{estacion_str} / {self.contaminante} / {self.fecha} hora {self.hora}: {self.valor} {self.unidad}"
