# Full-Stack Demo (Vuetify + FastAPI)

A monorepo demo application with a Vue 3 + Vuetify frontend and FastAPI backend.

## Prerequisites

- Python 3.10+
- Node.js 18+
- Docker & Docker Compose (optional)

## Project Structure

```
.
├── backend/          # FastAPI backend
│   ├── app/
│   │   └── main.py
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/         # Vue 3 + Vuetify frontend
│   ├── src/
│   ├── package.json
│   └── Dockerfile
├── docker/
├── docker-compose.yml
└── .env.example
```

## Local Development

### Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Backend runs at http://localhost:8000

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Frontend runs at http://localhost:5173

## Docker

```bash
cp .env.example .env
docker compose up
```

## Podman

```bash
cp .env.example .env
podman compose up
```


- Frontend: http://localhost:5173
- Backend: http://localhost:8000
- Health check: http://localhost:8000/health
