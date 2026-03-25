"""
Tareas Celery del app siniestros.
"""

from celery import shared_task
from django.core.cache import cache
from django.db.models import Count, Sum

CACHE_KEY = "estadisticas_siniestros"
CACHE_TTL  = 60 * 60 * 12  # 12 horas


def _calcular_estadisticas_siniestros() -> list[dict]:
    """
    Cuenta siniestros y suma lesionados/fallecidos por alcaldía y tipo de evento.
    """
    from .models import SiniestroVial

    return list(
        SiniestroVial.objects
        .values("alcaldia", "tipo_evento")
        .annotate(
            total=Count("id"),
            total_lesionados=Sum("lesionados"),
            total_fallecidos=Sum("fallecidos"),
        )
        .order_by("alcaldia", "tipo_evento")
    )


@shared_task(name="siniestros.calcular_estadisticas_siniestros", bind=True, max_retries=3)
def calcular_estadisticas_siniestros(self) -> int:
    """
    Calcula y cachea estadísticas de siniestros por alcaldía y tipo.
    Retorna el número de combinaciones calculadas.
    """
    try:
        stats = _calcular_estadisticas_siniestros()
        cache.set(CACHE_KEY, stats, timeout=CACHE_TTL)
        return len(stats)
    except Exception as exc:
        raise self.retry(exc=exc, countdown=60)
