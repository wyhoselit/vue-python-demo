# Deployment Process Documentation

This document describes the complete deployment process for the vue-python-demo application with full OpenTelemetry observability stack.

## Overview

The application consists of:
- **Frontend**: Vue.js application (served on port 5173 in dev, 80 via nginx in prod)
- **Backend**: FastAPI application (port 8000)
- **Observability Stack**: OpenTelemetry Collector, Prometheus, Grafana, Loki, Tempo

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2 (or `docker compose` plugin)
- Git

## Quick Start (Local Development)

```bash
# Clone the repository
git clone <repository-url>
cd vue-python-demo

# Start the full stack with observability
docker compose -f docker-compose.yml -f docker-compose.override.yml up -d --build

# Verify services are running
docker compose ps
```

## Service Access Points

| Service | URL | Credentials |
|---------|-----|-------------|
| Frontend | http://localhost:5173 | N/A |
| Backend API | http://localhost:8000 | N/A |
| API Docs (Swagger) | http://localhost:8000/docs | N/A |
| Prometheus | http://localhost:9090 | N/A |
| Grafana | http://localhost:3000 | admin / admin |
| Jaeger (Tempo) | http://localhost:16686 | N/A |
| Loki (via Grafana) | http://localhost:3000/explore | N/A |

## Configuration Files

### Docker Compose
- `docker-compose.override.yml`: Extends `docker-compose.yml` for local development. This file adds volume mounts for live code reloading, exposes different ports, and includes the full observability stack (OpenTelemetry Collector, Prometheus, Grafana, Loki, Tempo).

### Using Only Core Services

To run only the `backend` and `frontend` without the observability stack (useful for faster development cycles or lower resource usage), omit the override file:

```bash
podman-compose -f docker-compose.yml up -d --build
```


### Observability Configurations
- `observability/collector-config.yaml`: OTel Collector config
- `observability/prometheus.yml`: Prometheus scrape config
- `observability/alert.rules`: Prometheus alerting rules
- `observability/loki-config.yaml`: Loki configuration
- `observability/tempo-config.yaml`: Tempo configuration
- `observability/grafana/provisioning/`: Grafana datasources and dashboards

## Deployment Steps

### 1. Environment Setup
```bash
# Create .env file if needed
cp .env.example .env
# Edit .env with your configuration
```

### 2. Build and Start Services
```bash
# Pull latest images
docker compose -f docker-compose.yml -f docker-compose.override.yml pull

# Build custom images
docker compose -f docker-compose.yml -f docker-compose.override.yml build

# Start all services in detached mode
docker compose -f docker-compose.yml -f docker-compose.override.yml up -d
```

### 3. Verify Deployment
```bash
# Check all containers are healthy
docker compose ps

# Check backend health
curl http://localhost:8000/health

# Check frontend
curl http://localhost:5173

# Check Prometheus targets
curl http://localhost:9090/api/v1/targets
```

### 4. Configure Grafana
1. Open http://localhost:3000
2. Login with admin/admin
3. Change default password
4. Verify datasources are configured:
   - Prometheus (http://prometheus:9090)
   - Loki (http://loki:3100)
   - Tempo (http://tempo:3200)
5. Import or verify dashboards are provisioned

## Observability Verification

### Metrics (Prometheus)
- Query: `http_server_requests_seconds_count`
- Check: Targets UP in Status → Targets

### Traces (Tempo/Jaeger)
- Access Jaeger UI: http://localhost:16686
- Search for traces from backend and frontend

### Logs (Loki via Grafana)
- Go to Explore → Loki
- Query: `{service="backend"}` or `{service="frontend"}`

## Stopping the Stack

```bash
# Stop services
docker compose -f docker-compose.yml -f docker-compose.override.yml down

# Stop and remove volumes (clears all data)
docker compose -f docker-compose.yml -f docker-compose.override.yml down -v
```

## Cloud Run Deployment (GCP)

### 1. Build and Push Images
```bash
# Set your GCP project
export PROJECT_ID=your-project-id
export REGION=us-central1

# Build and push backend
docker build -t gcr.io/$PROJECT_ID/backend ./backend
docker push gcr.io/$PROJECT_ID/backend

# Build and push frontend
docker build -t gcr.io/$PROJECT_ID/frontend ./frontend
docker push gcr.io/$PROJECT_ID/frontend
```

### 2. Deploy to Cloud Run
```bash
# Deploy backend
gcloud run deploy backend \
  --image gcr.io/$PROJECT_ID/backend \
  --platform managed \
  --region $REGION \
  --allow-unauthenticated \
  --set-env-vars OTEL_EXPORTER_OTLP_ENDPOINT=https://otel-collector-<hash>.run.app

# Deploy frontend
gcloud run deploy frontend \
  --image gcr.io/$PROJECT_ID/frontend \
  --platform managed \
  --region $REGION \
  --allow-unauthenticated
```

### 3. Observability in Cloud Run
- Use Cloud Trace for distributed tracing
- Use Cloud Logging for log aggregation
- Use Cloud Monitoring for metrics
- Consider deploying OTel Collector as a separate Cloud Run service

## Troubleshooting

### Container Won't Start
```bash
# Check logs
docker compose logs <service-name>

# Common issues:
# - Port conflicts (check 5173, 8000, 9090, 3000, 3100, 3200, 4317, 4318)
# - Missing .env file
# - Docker volume permissions
```

### No Data in Grafana
1. Verify datasources are connected (Admin → Data sources)
2. Check Prometheus targets are UP
3. Verify OTel Collector is receiving data (logs)
4. Check network connectivity between services

### High Memory Usage
- Adjust OTel Collector memory limits in docker-compose.override.yml
- Configure sampling in collector-config.yaml
- Set retention policies in Tempo/Loki

## Rollback Procedure

```bash
# Rollback to previous image
docker compose -f docker-compose.yml -f docker-compose.override.yml down
# Update image tags to previous version in .env or docker-compose.override.yml
docker compose -f docker-compose.yml -f docker-compose.override.yml up -d
```

## Monitoring Checklist

- [ ] All services show "healthy" in `docker compose ps`
- [ ] Prometheus targets are UP
- [ ] Grafana datasources are green
- [ ] Traces appear in Tempo/Jaeger
- [ ] Logs appear in Loki
- [ ] Dashboards render without errors
- [ ] Alerts are firing correctly (if configured)
- [ ] Frontend loads without console errors
- [ ] Backend API responds to /health endpoint