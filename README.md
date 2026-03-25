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

Common filters: `?linea=Linea+1` · `?anio=2023` · `?source=simple|desglosada` · `?sistema=cablebus|trolebus|tren_ligero`

---

### `seguridad` — FGJ investigation files

| Endpoint | Description |
|----------|-------------|
| `GET /api/v1/seguridad/carpetas/` | Investigation files (2016–2019) |
| `GET /api/v1/seguridad/carpetas/{id}/` | Detail |

Filters: `?alcaldia_hechos=CUAUHTÉMOC` · `?categoria_delito=DELITO+DE+ALTO+IMPACTO` · `?ao_hechos=2018`
Search: `?search=robo`

**Source:** ~808,871 records · resource_id `3f308147-b1fc-49a9-92b7-e74f3f79aa9c`

---

### `riesgos` — Risk atlas and shelters

| Endpoint | Description |
|----------|-------------|
| `GET /api/v1/riesgos/inundaciones/` | Flood risk by AGEB |
| `GET /api/v1/riesgos/refugios/` | Temporary shelters |

Flood filters: `?alcaldia=Xochimilco` · `?intensidad=Alto|Medio|Bajo` · `?r_p_v_e=Peligro`
Shelter filters: `?delegacion=Cuauhtémoc` · Search: `?search=deportivo`

---

## Project structure

```
data-cdmx-backend-django/
├── config/
│   ├── settings.py          # Main configuration (PostgreSQL, DRF, Celery, Redis)
│   ├── settings_test.py     # SQLite override for tests
│   ├── celery.py            # Celery app initialization
│   └── urls.py              # Root URL dispatcher
├── colonias/
│   ├── models.py            # Colonia
│   ├── serializers.py
│   ├── views.py             # ColoniaViewSet
│   ├── urls.py
│   ├── admin.py
│   └── tests.py             # 10 tests
├── transporte/
│   ├── models.py            # AfluenciaMetro, AfluenciaMetrobus, AfluenciaSTE, AfluenciaRTP
│   ├── serializers.py
│   ├── views.py             # 4 ViewSets
│   ├── tasks.py             # Celery tasks: ridership summaries
│   ├── urls.py
│   ├── admin.py
│   └── tests.py             # 12 tests
├── seguridad/
│   ├── models.py            # CarpetaInvestigacion
│   ├── serializers.py
│   ├── views.py             # CarpetaInvestigacionViewSet
│   ├── tasks.py             # Celery tasks: crime statistics
│   ├── urls.py
│   ├── admin.py
│   └── tests.py             # 8 tests
├── riesgos/
│   ├── models.py            # RiesgoInundacion, Refugio
│   ├── serializers.py
│   ├── views.py             # 2 ViewSets
│   ├── urls.py
│   ├── admin.py
│   └── tests.py             # 11 tests
├── .env.example
└── requirements.txt
```

## Quick start

### 1. PostgreSQL

```bash
docker run -d --name cdmx-postgres \
  -e POSTGRES_DB=cdmx \
  -e POSTGRES_USER=cdmx \
  -e POSTGRES_PASSWORD=cdmx \
  -p 5432:5432 postgres:16-alpine
```

### 2. Django backend

```bash
pip install -r requirements.txt
cp .env.example .env          # adjust credentials if needed

python3 manage.py migrate
python3 manage.py createsuperuser   # to access the admin
python3 manage.py runserver
```

API available at `http://localhost:8000/api/v1/`
Admin at `http://localhost:8000/admin/`

### 3. Load data

Run the pipeline from the [`cdmx-api-pipeline`](../cdmx-api-pipeline) repo. The DAGs write directly into the same PostgreSQL database.

## Testing

Tests use SQLite in memory — PostgreSQL is not required.

```bash
python3 manage.py test colonias transporte seguridad riesgos \
  --settings=config.settings_test -v 2
```

```
colonias    10 tests  — model (str, unique, nullable), API (list, retrieve, filter, search, read-only, fields)
transporte  12 tests  — AfluenciaMetro (unique_together, source), AfluenciaSTE (sistema_display), API filters
seguridad    8 tests  — CarpetaInvestigacion (str, unique, coords), API (list, filter, search, read-only)
riesgos     11 tests  — RiesgoInundacion + Refugio (str, unique), API (list, filters, search)
──────────────────────
Total       41 tests
```

## Environment variables

| Variable | Default | Description |
|----------|---------|-------------|
| `DJANGO_SECRET_KEY` | insecure-key | Secret key (change in production) |
| `DJANGO_DEBUG` | `true` | Debug mode |
| `DJANGO_ALLOWED_HOSTS` | `localhost 127.0.0.1` | Allowed hosts |
| `DB_NAME` | `cdmx` | Database name |
| `DB_USER` | `cdmx` | PostgreSQL user |
| `DB_PASSWORD` | `cdmx` | Password |
| `DB_HOST` | `localhost` | PostgreSQL host |
| `DB_PORT` | `5432` | Port |
| `REDIS_URL` | `redis://127.0.0.1:6379/0` | Redis URL for Django cache and Celery broker |

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
