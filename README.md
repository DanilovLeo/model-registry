# Model Registry

FastAPI-based ML Model Registry for tracking, versioning, and discovering trained models across teams.

**Tech Stack**: FastAPI + Tortoise ORM + PostgreSQL + Aerich + Pydantic v2

## Quick Start

```bash
docker-compose up --build -d
docker-compose exec app aerich init-db
curl http://localhost:8000/health
```

**Docs**: http://localhost:8000/docs | **Test**: `./test_api.sh`

---

## Database Schema

```
Team → Model → ModelVersion ← Tag (M2M)
                    ↓
                Dataset
```

| Entity | Unique Constraint | Key Fields |
|--------|-------------------|------------|
| **Team** | `name` | name, description |
| **Model** | `(name, team_id)` | name, team_id, description |
| **ModelVersion** | `(version, model_id)` | version, artifact_path, stage, framework, metrics (JSONB), hyperparameters (JSONB), created_by |
| **Dataset** | - | name, path, metadata (JSONB) |
| **Tag** | `(key, value)` | key, value |

**Features**: Soft deletes, JSONB metadata, async queries, stage lifecycle (DEV→STAGING→PROD→ARCHIVED)

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/teams` | Create team |
| GET | `/api/v1/teams` | List teams |
| POST | `/api/v1/teams/{id}/models` | Register model |
| GET | `/api/v1/models` | List all models |
| GET | `/api/v1/models/{id}` | Get model details |
| POST | `/api/v1/models/{id}/versions` | Create version |
| GET | `/api/v1/models/{id}/versions` | List versions |
| PATCH | `/api/v1/models/{id}/versions/{id}/stage` | Promote/demote stage |
| GET | `/api/v1/search?q=...&framework=...&stage=...&tags=...` | Search models |
| POST | `/api/v1/import/scan` | Import legacy models |

---

## Usage Examples

### Create Version with Metadata

```bash
curl -X POST http://localhost:8000/api/v1/models/1/versions \
  -H "Content-Type: application/json" \
  -d '{
    "version": "1.0.0",
    "artifact_path": "/models/ranking/v1.0.0",
    "framework": "pytorch",
    "stage": "DEVELOPMENT",
    "metrics": {"accuracy": 0.91, "f1": 0.87},
    "hyperparameters": {"lr": 0.001, "batch_size": 32},
    "created_by": "data_scientist"
  }'
```

### Promote to Production

```bash
curl -X PATCH http://localhost:8000/api/v1/models/1/versions/1/stage \
  -H "Content-Type: application/json" -d '{"stage": "PRODUCTION"}'
```

### Import Legacy Models

```bash
curl -X POST http://localhost:8000/api/v1/import/scan \
  -H "Content-Type: application/json" -d '{"path": "/app/models"}'
```

**Import Logic**: Parses `models/team_name/model_name_v1/` → extracts team, model name, version, detects framework from file extensions

---

## Project Structure

```
app/
  main.py              # FastAPI app
  database.py          # Tortoise config
  models/              # ORM models (5 entities)
  schemas/             # Pydantic schemas
  crud/                # DB operations
  routers/             # API endpoints
  services/
    import_scanner.py  # Legacy import
diagrams/              # 8 PlantUML diagrams
```

**Architecture**: `Client → Router → Schema → CRUD → ORM → PostgreSQL`

---

## Development

### Local (without Docker)

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
export DATABASE_URL="postgres://user:pass@localhost:5432/modelregistry"
uvicorn app.main:app --reload
```

### Migrations

```bash
aerich init-db                         # First time
aerich migrate --name "description"    # After model changes
aerich upgrade                         # Apply
```

### Makefile

```bash
make up         # Start services
make init-db    # Initialize DB
make logs       # View logs
make shell      # Container shell
make clean      # Remove all
```

---

## Common Commands

| Task | Command |
|------|---------|
| View logs | `docker-compose logs -f app` |
| Access shell | `docker-compose exec app bash` |
| Access DB | `docker-compose exec db psql -U modelregistry -d modelregistry` |
| Restart | `docker-compose restart` |
| Stop | `docker-compose down` |
| Full reset | `docker-compose down -v && rm -rf migrations/` |

---

## Troubleshooting

**"Connection refused"**: Wait 10-20s for PostgreSQL. Check: `docker-compose ps`

**"Table doesn't exist"**: Run `docker-compose exec app aerich init-db`

**Port conflict**: Edit `docker-compose.yml` ports: `"8001:8000"`

**Reset everything**:
```bash
docker-compose down -v && rm -rf migrations/
docker-compose up --build -d
docker-compose exec app aerich init-db
```

---

## Documentation

- **API**: http://localhost:8000/docs
- **Diagrams**: `diagrams/` (database, API, deployment, use cases, state, etc.)
- **Test**: `./test_api.sh`
