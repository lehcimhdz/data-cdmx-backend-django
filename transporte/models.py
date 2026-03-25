from django.db import models


class AfluenciaBase(models.Model):
    """Campos comunes a todos los sistemas de transporte."""

    ckan_id = models.IntegerField()
    fecha = models.DateField()
    anio = models.IntegerField()
    mes = models.CharField(max_length=20)
    afluencia = models.BigIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class AfluenciaMetro(AfluenciaBase):
    """
    Afluencia diaria del Metro CDMX.

    Consolida dataset simple (desde 2010) y desglosada (desde 2021)
    en una sola tabla. El campo ``source`` distingue el origen.

    Fuentes:
    - Simple:      resource_id=0e8ffe58-28bb-4dde-afcd-e5f5b4de4ccb (~1.1 M registros)
    - Desglosada:  resource_id=cce544e1-dc6b-42b4-bc27-0d8e6eb3ed72 (~1.08 M registros)
    """

    SIMPLE = "simple"
    DESGLOSADA = "desglosada"
    SOURCE_CHOICES = [(SIMPLE, "Simple"), (DESGLOSADA, "Desglosada")]

    source = models.CharField(max_length=12, choices=SOURCE_CHOICES)
    linea = models.CharField(max_length=50)
    estacion = models.CharField(max_length=100)
    tipo_pago = models.CharField(max_length=50, blank=True)

    class Meta:
        unique_together = [("ckan_id", "source")]
        ordering = ["-fecha", "linea", "estacion"]
        verbose_name = "Afluencia Metro"
        verbose_name_plural = "Afluencias Metro"

    def __str__(self) -> str:
        return f"Metro {self.linea} – {self.estacion} ({self.fecha})"


class AfluenciaMetrobus(AfluenciaBase):
    """
    Afluencia diaria de Metrobús CDMX.

    Fuentes:
    - Simple:      resource_id=f7943c47-835d-4078-93ea-906f64b72f3b (~52 K)
    - Desglosada:  resource_id=d122639e-a56a-4f26-a8b7-983464d11aaa (~26 K)
    """

    SIMPLE = "simple"
    DESGLOSADA = "desglosada"
    SOURCE_CHOICES = [(SIMPLE, "Simple"), (DESGLOSADA, "Desglosada")]

    source = models.CharField(max_length=12, choices=SOURCE_CHOICES)
    linea = models.CharField(max_length=50)
    tipo_pago = models.CharField(max_length=50, blank=True)

    class Meta:
        unique_together = [("ckan_id", "source")]
        ordering = ["-fecha", "linea"]
        verbose_name = "Afluencia Metrobús"
        verbose_name_plural = "Afluencias Metrobús"

    def __str__(self) -> str:
        return f"Metrobús {self.linea} ({self.fecha})"


class AfluenciaSTE(AfluenciaBase):
    """
    Afluencia de los Servicios de Transportes Eléctricos:
    Tren Ligero, Cablebus y Trolebús.

    Fuentes:
    - Tren Ligero: resource_id=c6f15e48-791d-4ed6-adc3-8d93ed80a055 (~3 K)
    - Cablebus:    resource_id=176c0d20-0111-43bc-903c-d7e807ff37c0 (~6.5 K)
    - Trolebús:    resource_id=48fdccd2-f910-4328-a018-df25b6a05b0b (~52 K)
    """

    TREN_LIGERO = "tren_ligero"
    CABLEBUS = "cablebus"
    TROLEBUS = "trolebus"
    SISTEMA_CHOICES = [
        (TREN_LIGERO, "Tren Ligero"),
        (CABLEBUS, "Cablebus"),
        (TROLEBUS, "Trolebús"),
    ]

    sistema = models.CharField(max_length=12, choices=SISTEMA_CHOICES)
    linea = models.CharField(max_length=50, blank=True)
    tipo_pago = models.CharField(max_length=50)

    class Meta:
        unique_together = [("ckan_id", "sistema")]
        ordering = ["-fecha", "sistema"]
        verbose_name = "Afluencia STE"
        verbose_name_plural = "Afluencias STE"

    def __str__(self) -> str:
        return f"STE {self.get_sistema_display()} ({self.fecha})"


class AfluenciaRTP(AfluenciaBase):
    """
    Afluencia diaria de la Red de Transporte de Pasajeros.

    Fuente: resource_id=a527d822-58ca-4140-ba91-ede5f10d8cb3 (~36.7 K)
    """

    ckan_id = models.IntegerField(unique=True)
    servicio = models.CharField(max_length=100)
    tipo_pago = models.CharField(max_length=50)

    class Meta:
        ordering = ["-fecha", "servicio"]
        verbose_name = "Afluencia RTP"
        verbose_name_plural = "Afluencias RTP"

    def __str__(self) -> str:
        return f"RTP {self.servicio} ({self.fecha})"
