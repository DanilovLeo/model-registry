# Model Registry API

FastAPI-based ML Model Registry for tracking, versioning, and discovering trained models across teams.

**Tech Stack**: FastAPI + Tortoise ORM + PostgreSQL + Aerich + Pydantic v2

## Quick Start
```bash
cp .env.example .env
docker-compose up --build -d
docker-compose exec app aerich init-db
```

**API Docs**: http://localhost:8000/docs | **Test**: `./test_api.sh`

## Project Structure
```
model-registry/
├── app/
│   ├── main.py              # FastAPI app
│   ├── database.py          # Tortoise config
│   ├── models/              # ORM models (5 entities)
│   ├── schemas/             # Pydantic schemas
│   ├── crud/                # DB operations
│   ├── routers/             # API endpoints
│   └── services/
│       └── import_scanner.py  # Legacy import
├── models/                  # Legacy model directory (import demo)
├── diagrams/                # PlantUML architecture diagrams
├── .env.example
├── docker-compose.yml
├── Dockerfile
├── pyproject.toml
└── requirements.txt
```

## Common Commands

| Task | Command |
|------|---------|
| View logs | `docker-compose logs -f app` |
| Access DB | `docker-compose exec db psql -U modelregistry -d modelregistry` |
| Stop | `docker-compose down` |
| Full reset | `docker-compose down -v && docker-compose up --build -d && docker-compose exec app aerich init-db` |

## Migrations
```bash
aerich migrate --name "description"   # After model changes
aerich upgrade                         # Apply
```
