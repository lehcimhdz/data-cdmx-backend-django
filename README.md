# data-cdmx-backend-django

Backend Django REST que expone los datos abiertos de la Ciudad de México a través de una API. Los datos son cargados por el pipeline ETL [`cdmx-api-pipeline`](../cdmx-api-pipeline) desde el portal [datos.cdmx.gob.mx](https://datos.cdmx.gob.mx).

## Arquitectura

```
cdmx-api-pipeline  ──►  PostgreSQL  ◄──  Django REST API  ──►  Clientes
   (Airflow ETL)          (datos)         (este repo)
```

Django define el schema (modelos + migraciones). Airflow escribe los datos vía upsert directo. Django los expone como API de solo lectura.

## Apps y endpoints

### `colonias` — Catálogo de colonias

| Endpoint | Descripción |
|----------|-------------|
| `GET /api/v1/colonias/` | Lista paginada |
| `GET /api/v1/colonias/{id}/` | Detalle |

Filtros: `?cve_dleg=16` · Búsqueda: `?search=tepito` · Orden: `?ordering=nombre`

**Fuente:** ~1,812 colonias · resource_id `03368e1e-f05e-4bea-ac17-58fc650f6fee`

---

### `transporte` — Afluencia de transporte público

| Endpoint | Sistema | Registros |
|----------|---------|-----------|
| `GET /api/v1/transporte/metro/` | Metro CDMX (simple 2010– + desglosada 2021–) | ~2.2 M |
| `GET /api/v1/transporte/metrobus/` | Metrobús (simple 2005– + desglosada 2021–) | ~78 K |
| `GET /api/v1/transporte/ste/` | Tren Ligero, Cablebus, Trolebús (2022–) | ~62 K |
| `GET /api/v1/transporte/rtp/` | Red de Transporte de Pasajeros (2022–) | ~37 K |

Filtros comunes: `?linea=Linea+1` · `?anio=2023` · `?source=simple|desglosada` · `?sistema=cablebus|trolebus|tren_ligero`

---

### `seguridad` — Carpetas de investigación FGJ

| Endpoint | Descripción |
|----------|-------------|
| `GET /api/v1/seguridad/carpetas/` | Carpetas de investigación (2016–2019) |
| `GET /api/v1/seguridad/carpetas/{id}/` | Detalle |

Filtros: `?alcaldia_hechos=CUAUHTÉMOC` · `?categoria_delito=DELITO+DE+ALTO+IMPACTO` · `?ao_hechos=2018`
Búsqueda: `?search=robo`

**Fuente:** ~808,871 registros · resource_id `3f308147-b1fc-49a9-92b7-e74f3f79aa9c`

---

### `riesgos` — Atlas de riesgo y refugios

| Endpoint | Descripción |
|----------|-------------|
| `GET /api/v1/riesgos/inundaciones/` | Riesgo de inundación por AGEB |
| `GET /api/v1/riesgos/refugios/` | Refugios temporales |

Filtros inundaciones: `?alcaldia=Xochimilco` · `?intensidad=Alto|Medio|Bajo` · `?r_p_v_e=Peligro`
Filtros refugios: `?delegacion=Cuauhtémoc` · Búsqueda: `?search=deportivo`

---

## Estructura del proyecto

```
data-cdmx-backend-django/
├── config/
│   ├── settings.py          # Configuración principal (PostgreSQL, DRF)
│   ├── settings_test.py     # Override con SQLite para tests
│   └── urls.py              # Rutas raíz
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
│   ├── urls.py
│   ├── admin.py
│   └── tests.py             # 12 tests
├── seguridad/
│   ├── models.py            # CarpetaInvestigacion
│   ├── serializers.py
│   ├── views.py             # CarpetaInvestigacionViewSet
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

## Inicio rápido

### 1. PostgreSQL

```bash
docker run -d --name cdmx-postgres \
  -e POSTGRES_DB=cdmx \
  -e POSTGRES_USER=cdmx \
  -e POSTGRES_PASSWORD=cdmx \
  -p 5432:5432 postgres:16-alpine
```

### 2. Backend Django

```bash
pip install -r requirements.txt
cp .env.example .env          # ajusta credenciales si es necesario

python3 manage.py migrate
python3 manage.py createsuperuser   # para acceder al admin
python3 manage.py runserver
```

La API estará en `http://localhost:8000/api/v1/`
El admin estará en `http://localhost:8000/admin/`

### 3. Cargar datos

Ejecuta el pipeline desde el repo [`cdmx-api-pipeline`](../cdmx-api-pipeline). Los DAGs escriben directamente en la misma base de datos PostgreSQL.

## Testing

Los tests usan SQLite en memoria — no requieren PostgreSQL corriendo.

```bash
python3 manage.py test colonias transporte seguridad riesgos \
  --settings=config.settings_test -v 2
```

```
colonias   10 tests  — modelo (str, unique, nullable), API (list, retrieve, filter, search, read-only, campos)
transporte 12 tests  — AfluenciaMetro (unique_together, source), AfluenciaSTE (sistema_display), API filtros
seguridad   8 tests  — CarpetaInvestigacion (str, unique, coords), API (list, filter, search, read-only)
riesgos    11 tests  — RiesgoInundacion + Refugio (str, unique), API (list, filtros, búsqueda)
─────────────────────
Total      41 tests
```

## Variables de entorno

| Variable | Default | Descripción |
|----------|---------|-------------|
| `DJANGO_SECRET_KEY` | insecure-key | Clave secreta (cambiar en producción) |
| `DJANGO_DEBUG` | `true` | Modo debug |
| `DJANGO_ALLOWED_HOSTS` | `localhost 127.0.0.1` | Hosts permitidos |
| `DB_NAME` | `cdmx` | Nombre de la BD |
| `DB_USER` | `cdmx` | Usuario de PostgreSQL |
| `DB_PASSWORD` | `cdmx` | Contraseña |
| `DB_HOST` | `localhost` | Host de PostgreSQL |
| `DB_PORT` | `5432` | Puerto |

## Modelos — referencia rápida

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
