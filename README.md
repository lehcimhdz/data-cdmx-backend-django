# data-cdmx-backend-django

Django REST backend that exposes Ciudad de México open data through a read-only API. Data is loaded by the ETL pipeline [`cdmx-api-pipeline`](../cdmx-api-pipeline) from [datos.cdmx.gob.mx](https://datos.cdmx.gob.mx).

## Architecture

```
cdmx-api-pipeline  ──►  PostgreSQL  ◄──  Django REST API  ──►  Clients
   (Airflow ETL)          (data)         (this repo)
```

Django owns the schema (models + migrations). Airflow writes data via direct upsert. Django exposes it as a read-only API.

## Apps and endpoints

### `colonias` — Colonias catalog

| Endpoint | Description |
|----------|-------------|
| `GET /api/v1/colonias/` | Paginated list |
| `GET /api/v1/colonias/{id}/` | Detail |

Filters: `?cve_dleg=16` · Search: `?search=tepito` · Sort: `?ordering=nombre`

**Source:** ~1,812 colonias · resource_id `03368e1e-f05e-4bea-ac17-58fc650f6fee`

---

### `transporte` — Public transit ridership

| Endpoint | System | Records |
|----------|--------|---------|
| `GET /api/v1/transporte/metro/` | Metro CDMX (simple 2010– + desglosada 2021–) | ~2.2 M |
| `GET /api/v1/transporte/metrobus/` | Metrobús (simple 2005– + desglosada 2021–) | ~78 K |
| `GET /api/v1/transporte/ste/` | Tren Ligero, Cablebus, Trolebús (2022–) | ~62 K |
| `GET /api/v1/transporte/rtp/` | Red de Transporte de Pasajeros (2022–) | ~37 K |

Common filters: `?linea=Linea+1` · `?anio=2023` · `?mes=Marzo` · `?source=simple|desglosada` · `?sistema=cablebus|trolebus|tren_ligero`

---

### `seguridad` — FGJ investigation files

| Endpoint | Description |
|----------|-------------|
| `GET /api/v1/seguridad/carpetas/` | Investigation files (2016–2019) |
| `GET /api/v1/seguridad/carpetas/{id}/` | Detail |

Filters: `?alcaldia_hechos=CUAUHTÉMOC` · `?categoria_delito=DELITO+DE+ALTO+IMPACTO` · `?ao_hechos=2018` · `?mes_hechos=JUNIO`
Search: `?search=robo`

**Source:** ~808,871 records · resource_id `3f308147-b1fc-49a9-92b7-e74f3f79aa9c`

---

### `riesgos` — Risk atlas and shelters

| Endpoint | Description |
|----------|-------------|
| `GET /api/v1/riesgos/inundaciones/` | Flood risk by AGEB |
| `GET /api/v1/riesgos/refugios/` | Temporary shelters |

Flood filters: `?alcaldia=Xochimilco` · `?intensidad=Alto|Medio|Bajo` · `?r_p_v_e=Peligro` · `?fenomeno=Inundacion`
Shelter filters: `?delegacion=Cuauhtémoc` · `?region=I` · Search: `?search=deportivo`

---

### System endpoints

| Endpoint | Description |
|----------|-------------|
| `GET /health/` | Health check — DB + Redis status (`200` / `503`) |
| `GET /api/docs/` | Swagger UI (interactive API explorer) |
| `GET /api/schema/` | OpenAPI schema (JSON/YAML) |
| `GET /admin/` | Django admin |

---

## Project structure

```
data-cdmx-backend-django/
├── config/
│   ├── settings.py          # Main config (PostgreSQL, DRF, Celery, Redis, Sentry, logging)
│   ├── settings_test.py     # SQLite + LocMemCache override for tests
│   ├── celery.py            # Celery app initialization
│   ├── views.py             # Health check view
│   └── urls.py              # Root URL dispatcher
├── colonias/                # Colonia model + ViewSet + tests
├── transporte/              # AfluenciaMetro/bus/STE/RTP models + ViewSets + Celery tasks + tests
├── seguridad/               # CarpetaInvestigacion model + ViewSet + Celery tasks + tests
├── riesgos/                 # RiesgoInundacion + Refugio models + ViewSets + tests
├── Dockerfile               # Multi-stage build (builder + runtime, non-root user)
├── Makefile                 # Common commands
├── pyproject.toml           # Ruff, black, pytest, coverage config
├── .pre-commit-config.yaml
├── .env.example
└── requirements.txt
```

## Quick start

```bash
cp .env.example .env

make db      # start PostgreSQL 16 container
make redis   # start Redis 7 container

pip install -r requirements.txt
make migrate
make run
```

| URL | What |
|-----|------|
| `http://localhost:8000/api/v1/` | API root |
| `http://localhost:8000/api/docs/` | Swagger UI |
| `http://localhost:8000/health/` | Health check |
| `http://localhost:8000/admin/` | Admin |

To load data, run the pipeline from [`cdmx-api-pipeline`](../cdmx-api-pipeline). The DAGs write directly into the same PostgreSQL database.

## Testing

Tests use SQLite in memory — no PostgreSQL or Redis required.

```bash
make test
```

```
colonias    10 tests  — model (str, unique, nullable), API (list, retrieve, filter, search, read-only)
transporte  12 tests  — AfluenciaMetro (unique_together, source), AfluenciaSTE, API filters
seguridad    8 tests  — CarpetaInvestigacion (str, unique, coords), API (list, filter, search)
riesgos     11 tests  — RiesgoInundacion + Refugio, API (list, filters, search)
──────────────────────
Total       41 tests
```

## Docker

```bash
docker build -t cdmx-backend .
docker run --env-file .env -p 8000:8000 cdmx-backend
```

The image uses a two-stage build — only the virtualenv and source are copied to the runtime stage. The app runs as a non-root user.

## Observability

### Health check

`GET /health/` returns `200` when both DB and Redis are reachable, `503` otherwise:

```json
{"status": "ok", "db": "ok", "redis": "ok"}
```

### Sentry

Set `SENTRY_DSN` in `.env` to enable error tracking for Django requests and Celery tasks.
`send_default_pii=False` by default. Set `DJANGO_ENV=production` to tag events correctly.

### Logging

| Environment | Format |
|-------------|--------|
| `DJANGO_DEBUG=true` (default) | Plain text |
| `DJANGO_DEBUG=false` | JSON — ready for CloudWatch Logs / Datadog |

## Rate limiting

Anonymous clients are limited to **200 requests/hour** (`AnonRateThrottle`).
Returns `HTTP 429` with a `Retry-After` header when exceeded.
Adjust `DEFAULT_THROTTLE_RATES` in `settings.py` to fit actual traffic.

## Environment variables

| Variable | Default | Description |
|----------|---------|-------------|
| `DJANGO_SECRET_KEY` | insecure-key | Secret key — always change in production |
| `DJANGO_DEBUG` | `true` | Debug mode — set `false` in production |
| `DJANGO_ALLOWED_HOSTS` | `localhost 127.0.0.1` | Space-separated allowed hosts |
| `DB_NAME` | `cdmx` | Database name |
| `DB_USER` | `cdmx` | PostgreSQL user |
| `DB_PASSWORD` | `cdmx` | Password |
| `DB_HOST` | `localhost` | PostgreSQL host |
| `DB_PORT` | `5432` | Port |
| `REDIS_URL` | `redis://127.0.0.1:6379/0` | Redis URL for cache and Celery broker |
| `SENTRY_DSN` | — | Sentry DSN (leave empty to disable) |
| `DJANGO_ENV` | `production` | Environment tag for Sentry |

## Models — quick reference

### Colonia
`ckan_id` · `nombre` · `clave` · `cvegeo` · `cve_dleg` · `lat` · `lon`

### AfluenciaMetro
`ckan_id` · `source` (simple/desglosada) · `fecha` · `anio` · `mes` · `linea` · `estacion` · `tipo_pago` · `afluencia`

### AfluenciaMetrobus
`ckan_id` · `source` · `fecha` · `anio` · `mes` · `linea` · `tipo_pago` · `afluencia`

### AfluenciaSTE
`ckan_id` · `sistema` (tren_ligero/cablebus/trolebus) · `fecha` · `anio` · `mes` · `linea` · `tipo_pago` · `afluencia`

### AfluenciaRTP
`ckan_id` · `fecha` · `anio` · `mes` · `servicio` · `tipo_pago` · `afluencia`

### CarpetaInvestigacion
`ckan_id` · `fecha_hecho` · `hora_hecho` · `delito` · `categoria_delito` · `fiscalia` · `agencia` · `alcaldia_hechos` · `colonia_datos` · `latitud` · `longitud`

### RiesgoInundacion
`ckan_id` · `fenomeno` · `taxonomia` · `intensidad` · `alcaldia` · `cvegeo` · `area_m2` · `period_ret` · `lat` · `lon`

### Refugio
`ckan_id` · `nombre` · `delegacion` · `colonia` · `calle_y_numero` · `cap_albergue` · `region` · `lat` · `lon`
