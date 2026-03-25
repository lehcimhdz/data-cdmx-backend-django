"""
Tareas Celery del app seguridad.
"""

from celery import shared_task
from django.core.cache import cache
from django.db.models import Count

CACHE_KEY_STATS  = "estadisticas_delitos"
CACHE_KEY_MAPA   = "mapa_calor_delitos"
CACHE_TTL        = 60 * 60 * 12  # 12 horas


# ---------------------------------------------------------------------------
# Lógica pura
# ---------------------------------------------------------------------------

def _calcular_estadisticas_delitos() -> list[dict]:
    """
    Cuenta carpetas de investigación agrupadas por alcaldía y categoría de delito.
    Ordenadas de mayor a menor frecuencia.
    """
    from .models import CarpetaInvestigacion

    return list(
        CarpetaInvestigacion.objects
        .exclude(alcaldia_hechos="")
        .values("alcaldia_hechos", "categoria_delito", "ao_hechos")
        .annotate(total=Count("id"))
        .order_by("-total")
    )


def _calcular_mapa_calor() -> list[dict]:
    """
    Retorna registros con coordenadas para un mapa de calor de delitos.
    Solo incluye registros con lat/lon válidos y categoría de alto impacto.
    """
    from .models import CarpetaInvestigacion

    return list(
        CarpetaInvestigacion.objects
        .filter(
            categoria_delito="DELITO DE ALTO IMPACTO",
            latitud__isnull=False,
            longitud__isnull=False,
        )
        .values("latitud", "longitud", "delito", "alcaldia_hechos", "ao_hechos")
    )


# ---------------------------------------------------------------------------
# Tareas Celery
# ---------------------------------------------------------------------------

@shared_task(name="seguridad.calcular_estadisticas_delitos", bind=True, max_retries=3)
def calcular_estadisticas_delitos(self) -> int:
    """
    Calcula y cachea estadísticas de delitos por alcaldía y categoría.
    Retorna el número de combinaciones calculadas.
    """
    try:
        stats = _calcular_estadisticas_delitos()
        cache.set(CACHE_KEY_STATS, stats, timeout=CACHE_TTL)
        return len(stats)
    except Exception as exc:
        raise self.retry(exc=exc, countdown=60)


@shared_task(name="seguridad.calcular_mapa_calor", bind=True, max_retries=3)
def calcular_mapa_calor(self) -> int:
    """
    Calcula y cachea puntos para el mapa de calor de delitos de alto impacto.
    """
    try:
        puntos = _calcular_mapa_calor()
        cache.set(CACHE_KEY_MAPA, puntos, timeout=CACHE_TTL)
        return len(puntos)
    except Exception as exc:
        raise self.retry(exc=exc, countdown=60)
