# SovereignAI — Docker Container Architecture & Operations

## 1. Services Overview

The multi-container application is defined in `docker-compose.yml`:

| Service | Image / Build | Internal Port | Exposed Port | Purpose | Health Check |
|---|---|---|---|---|---|
| **postgres** | `postgres:16-alpine` | 5432 | 5432 | Relational DB | `pg_isready` |
| **redis** | `redis:7-alpine` | 6379 | 6379 | Pub/Sub & Celery broker | `redis-cli ping` |
| **qdrant** | `qdrant/qdrant:v1.11.0` | 6333 | 6333 | Vector search database | Port check |
| **ollama** | `ollama/ollama:latest` | 11434 | 11434 | Local LLM inference server | API `/api/version` |
| **backend** | `./backend` | 8000 | 8001 | FastAPI async backend | `/health` endpoint |
| **ai-engine** | `./ai-engine` | 9000 | 9000 | Multimodal worker microservice | Port probe |
| **celery-worker**| `./backend` | N/A | N/A | Background task processing | Celery ping |
| **frontend** | `./frontend` | 3000 | 3000 | Next.js 16 operator workspace | HTTP probe |

---

## 2. Persistent Named Volumes (Rule 49)

Under no circumstances should `docker compose down -v` be run during standard operations.
All state is stored in persistent named volumes:

- `sovereignai_pgdata`: PostgreSQL data directory (`/var/lib/postgresql/data`)
- `sovereignai_redisdata`: Redis append-only / snapshot persistence (`/data`)
- `sovereignai_qdrantdata`: Qdrant vector index storage (`/qdrant/storage`)
- `sovereignai_ollamadata`: Downloaded model weights (`/root/.ollama`)

---

## 3. Operations Cheat Sheet

```bash
# Start all containers in detached mode
scripts\start.bat

# Stop containers gracefully (preserves all volume data)
scripts\stop.bat

# View container logs
docker compose logs -f backend
docker compose logs -f celery-worker

# Rebuild containers after code modifications
docker compose build

# Inspect container health
scripts\status.bat
```
