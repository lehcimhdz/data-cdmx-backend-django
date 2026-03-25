import logging

from django.core.cache import cache
from django.db import connection
from django.http import JsonResponse

logger = logging.getLogger(__name__)


def health(request):
    status = {}
    http_status = 200

    # Database
    try:
        connection.ensure_connection()
        status["db"] = "ok"
    except Exception as exc:
        logger.error("Health check — DB error: %s", exc)
        status["db"] = "error"
        http_status = 503

    # Redis
    try:
        cache.set("_health", "1", timeout=5)
        cache.get("_health")
        status["redis"] = "ok"
    except Exception as exc:
        logger.error("Health check — Redis error: %s", exc)
        status["redis"] = "error"
        http_status = 503

    status["status"] = "ok" if http_status == 200 else "error"
    return JsonResponse(status, status=http_status)
