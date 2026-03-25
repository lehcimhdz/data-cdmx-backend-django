"""
Tareas Celery del app transporte.

Las funciones privadas (_calcular_*) contienen la lógica pura y son
testeables sin un broker. Las tareas decoradas con @shared_task las
envuelven y cachean el resultado en Redis.
"""

from celery import shared_task
from django.core.cache import cache
from django.db.models import Sum

CACHE_KEY_METRO = "resumen_afluencia_metro"
CACHE_KEY_STE   = "resumen_afluencia_ste"
CACHE_TTL       = 60 * 60 * 6  # 6 horas


# ---------------------------------------------------------------------------
# Lógica pura (testeable sin Celery)
# ---------------------------------------------------------------------------

def _calcular_resumen_metro() -> list[dict]:
    """
    Suma afluencia del Metro por línea, año y mes usando el dataset simple
    (cobertura desde 2010, sin desglose por tipo de pago).
    """
    from .models import AfluenciaMetro

    return list(
        AfluenciaMetro.objects
        .filter(source=AfluenciaMetro.SIMPLE)
        .values("linea", "anio", "mes")
        .annotate(total_afluencia=Sum("afluencia"))
        .order_by("-anio", "linea")
    )


def _calcular_resumen_ste() -> list[dict]:
    """
    Suma afluencia de los Servicios de Transportes Eléctricos
    (Cablebus, Trolebús, Tren Ligero) por sistema, línea, año y mes.
    """
    from .models import AfluenciaSTE

    return list(
        AfluenciaSTE.objects
        .values("sistema", "linea", "anio", "mes")
        .annotate(total_afluencia=Sum("afluencia"))
        .order_by("-anio", "sistema")
    )


# ---------------------------------------------------------------------------
# Tareas Celery
# ---------------------------------------------------------------------------

@shared_task(name="transporte.calcular_resumen_metro", bind=True, max_retries=3)
def calcular_resumen_metro(self) -> int:
    """
    Calcula y cachea el resumen mensual de afluencia del Metro por línea.
    Retorna el número de combinaciones línea/año/mes calculadas.
    """
    try:
        resumen = _calcular_resumen_metro()
        cache.set(CACHE_KEY_METRO, resumen, timeout=CACHE_TTL)
        return len(resumen)
    except Exception as exc:
        raise self.retry(exc=exc, countdown=60)


@shared_task(name="transporte.calcular_resumen_ste", bind=True, max_retries=3)
def calcular_resumen_ste(self) -> int:
    """
    Calcula y cachea el resumen mensual de afluencia de los STE.
    Retorna el número de combinaciones sistema/línea/año/mes calculadas.
    """
    try:
        resumen = _calcular_resumen_ste()
        cache.set(CACHE_KEY_STE, resumen, timeout=CACHE_TTL)
        return len(resumen)
    except Exception as exc:
        raise self.retry(exc=exc, countdown=60)
