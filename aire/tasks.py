"""
Tareas Celery del app aire.

La función privada _calcular_indice_calidad_aire contiene la lógica pura
y es testeable sin un broker. La tarea decorada la envuelve y cachea en Redis.
"""

from celery import shared_task
from django.core.cache import cache
from django.db.models import Avg, Max

CACHE_KEY_AQI = "indice_calidad_aire"
CACHE_TTL = 60 * 60  # 1 hora


def _calcular_indice_calidad_aire() -> list[dict]:
    """
    Retorna el valor promedio más reciente de cada contaminante por estación.
    Usa la última fecha disponible para cada combinación estacion+contaminante.
    """
    from .models import Lectura

    # Fecha más reciente por estación y contaminante
    ultima_fecha = (
        Lectura.objects
        .values("estacion_id", "contaminante")
        .annotate(ultima=Max("fecha"))
    )
    mapping = {(r["estacion_id"], r["contaminante"]): r["ultima"] for r in ultima_fecha}

    result = []
    for (estacion_id, contaminante), fecha in mapping.items():
        promedio = (
            Lectura.objects
            .filter(estacion_id=estacion_id, contaminante=contaminante, fecha=fecha)
            .aggregate(promedio=Avg("valor"))
        )
        result.append({
            "estacion_id": estacion_id,
            "contaminante": contaminante,
            "fecha": str(fecha),
            "promedio": promedio["promedio"],
        })

    return sorted(result, key=lambda x: (x["estacion_id"] or 0, x["contaminante"]))


@shared_task(name="aire.calcular_indice_calidad_aire", bind=True, max_retries=3)
def calcular_indice_calidad_aire(self) -> int:
    """
    Calcula y cachea el índice de calidad del aire más reciente por estación.
    Retorna el número de combinaciones estación/contaminante calculadas.
    """
    try:
        indice = _calcular_indice_calidad_aire()
        cache.set(CACHE_KEY_AQI, indice, timeout=CACHE_TTL)
        return len(indice)
    except Exception as exc:
        raise self.retry(exc=exc, countdown=60)
