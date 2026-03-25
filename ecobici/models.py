from django.db import models


class CicloEstacion(models.Model):
    """
    Estaciones de ECOBICI (bicicletas compartidas CDMX).

    Fuente: resource_id=5fbacfcc-f677-406c-9356-6ced541240fe (~989 registros)
    Campos API: _id, sistema, num_cicloe, calle_prin, calle_secu, colonia,
                alcaldia, latitud, longitud, sitio_de_e, estatus
    """

    ckan_id = models.IntegerField(unique=True)

    sistema = models.CharField(max_length=100, blank=True)
    num_cicloe = models.CharField(max_length=50, blank=True, help_text="Número de cicloe-stación")
    calle_prin = models.CharField(max_length=255, blank=True, help_text="Calle principal")
    calle_secu = models.CharField(max_length=255, blank=True, help_text="Calle secundaria")
    colonia = models.CharField(max_length=255, blank=True)
    alcaldia = models.CharField(max_length=100, blank=True)
    latitud = models.FloatField(null=True, blank=True)
    longitud = models.FloatField(null=True, blank=True)
    sitio_de_e = models.CharField(max_length=255, blank=True, help_text="Sitio de estación")
    estatus = models.CharField(max_length=50, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["alcaldia", "num_cicloe"]
        indexes = [
            models.Index(fields=["alcaldia"]),
            models.Index(fields=["estatus"]),
        ]
        verbose_name = "Cicloestación ECOBICI"
        verbose_name_plural = "Cicloestaciones ECOBICI"

    def __str__(self) -> str:
        return f"{self.num_cicloe} – {self.calle_prin} ({self.alcaldia})"


class ViajesDiarios(models.Model):
    """
    Viajes diarios ECOBICI agregados por fecha y género.

    Fuente: resource_id=4df66c20-f969-4b3e-9bce-34987da33bc1
    Campos API: _id, anio, mes, fecha, genero, viajes
    """

    ckan_id = models.IntegerField(unique=True)

    anio = models.IntegerField(null=True, blank=True)
    mes = models.IntegerField(null=True, blank=True)
    fecha = models.DateField(null=True, blank=True)
    genero = models.CharField(max_length=50, blank=True)
    viajes = models.IntegerField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-fecha", "genero"]
        indexes = [
            models.Index(fields=["fecha"]),
            models.Index(fields=["genero"]),
            models.Index(fields=["anio", "mes"]),
        ]
        verbose_name = "Viajes Diarios ECOBICI"
        verbose_name_plural = "Viajes Diarios ECOBICI"

    def __str__(self) -> str:
        return f"{self.fecha} / {self.genero}: {self.viajes} viajes"


class ViajesDesglosados(models.Model):
    """
    Viajes ECOBICI desglosados por hora, género y rango de edad.

    Fuente: resource_id=2a1cfcab-61ce-46c9-ab7e-7ea1053e6d04 (~11,773 registros)
    Campos API: _id, anio, mes, fecha_corte, hora, genero, rango_edad, viajes
    """

    ckan_id = models.IntegerField(unique=True)

    anio = models.IntegerField(null=True, blank=True)
    mes = models.IntegerField(null=True, blank=True)
    fecha_corte = models.DateField(null=True, blank=True)
    hora = models.IntegerField(null=True, blank=True, help_text="Hora del día (0–23)")
    genero = models.CharField(max_length=50, blank=True)
    rango_edad = models.CharField(max_length=50, blank=True)
    viajes = models.IntegerField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-fecha_corte", "hora", "genero"]
        indexes = [
            models.Index(fields=["fecha_corte"]),
            models.Index(fields=["genero"]),
            models.Index(fields=["anio", "mes"]),
        ]
        verbose_name = "Viajes Desglosados ECOBICI"
        verbose_name_plural = "Viajes Desglosados ECOBICI"

    def __str__(self) -> str:
        return f"{self.fecha_corte} / hora {self.hora} / {self.genero} / {self.rango_edad}"
