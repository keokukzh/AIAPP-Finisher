# Local Multi-Container Deployment (Docker Compose)

This guide describes how to run the APP-Finisher stack locally using Docker Compose with bundled infrastructure (MongoDB, Redis, Prometheus, Grafana).

## Prerequisites
- Docker Desktop (20.10+)
- Docker Compose V2 (`docker compose`)

## Quick Start
```bash
# Build images
docker compose build

# Start stack
docker compose up -d

# Follow logs for API and UI
docker compose logs -f ai-project-manager

# Stop stack
docker compose down

# Clean all volumes (data loss!)
docker compose down -v
```

## Services
- API (FastAPI): http://localhost:${API_PORT:-8000}
- UI (Streamlit): http://localhost:${UI_PORT:-8501}
- MongoDB: localhost:${MONGO_PORT:-27017}
- Redis: localhost:${REDIS_PORT:-6379}
- Prometheus: http://localhost:${PROMETHEUS_PORT:-9090}
- Grafana: http://localhost:${GRAFANA_PORT:-3000}

## Healthchecks
- API: `GET /status`
- UI: Streamlit internal `_stcore/health`
- MongoDB: `mongosh --eval 'db.runCommand({ ping: 1 })'`
- Redis: `redis-cli ping`

## Environment
Create a `.env` file in the project root (values shown are defaults):
```
API_PORT=8000
UI_PORT=8501
MONGO_PORT=27017
REDIS_PORT=6379
PROMETHEUS_PORT=9090
GRAFANA_PORT=3000
MONGODB_URL=mongodb://mongodb:27017/appfinisher
REDIS_URL=redis://redis:6379/0
FASTAPI_URL=http://api:8000
PROJECT_PATH=/app
LOG_LEVEL=INFO
GRAFANA_USER=admin
GRAFANA_PASSWORD=admin
```

## Validation Checklist
- `curl http://localhost:8000/status` returns healthy JSON
- Open `http://localhost:8000/docs`
- Open `http://localhost:8501` (UI calls API successfully)
- Prometheus targets up at `/targets`
- Grafana accessible with default creds

## Notes
- For live dev, use `docker-compose.dev.yml` (hot reload mounts)
- For production-like runs, use the default `docker-compose.yml` with no bind mounts
- Keep API keys in your local environment or a private `.env` (gitignored)
