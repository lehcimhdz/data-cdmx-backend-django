.PHONY: run migrate test lint fmt shell help

# ── Development ──────────────────────────────────────────────────────────────

run:
	python3 manage.py runserver

migrate:
	python3 manage.py migrate

migrations:
	python3 manage.py makemigrations

shell:
	python3 manage.py shell

collectstatic:
	python3 manage.py collectstatic --noinput

# ── Tests & quality ──────────────────────────────────────────────────────────

test:
	python3 manage.py test colonias transporte seguridad riesgos \
		--settings=config.settings_test -v 2

coverage:
	python3 -m pytest --cov=colonias --cov=transporte --cov=seguridad --cov=riesgos \
		--cov-report=term-missing --cov-fail-under=80

lint:
	ruff check .

fmt:
	ruff format .

# ── Docker (local DB + Redis) ─────────────────────────────────────────────────

db:
	docker run -d --name cdmx-postgres \
		-e POSTGRES_DB=cdmx \
		-e POSTGRES_USER=cdmx \
		-e POSTGRES_PASSWORD=cdmx \
		-p 5432:5432 postgres:16-alpine

redis:
	docker run -d --name cdmx-redis \
		-p 6379:6379 redis:7-alpine

# ── Help ──────────────────────────────────────────────────────────────────────

help:
	@echo ""
	@echo "  run            Start Django development server"
	@echo "  migrate        Apply database migrations"
	@echo "  migrations     Generate new migration files"
	@echo "  shell          Open Django shell"
	@echo "  collectstatic  Collect static files"
	@echo "  test           Run all tests (SQLite, no infra required)"
	@echo "  coverage       Run tests with coverage report (min 80%)"
	@echo "  lint           Run ruff linter"
	@echo "  fmt            Run ruff formatter"
	@echo "  db             Start a local PostgreSQL 16 container"
	@echo "  redis          Start a local Redis 7 container"
	@echo ""
