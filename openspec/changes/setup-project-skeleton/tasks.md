## 1. Project Structure Setup

- [x] 1.1 Create `backend/`, `frontend/`, `docker/` directories
- [x] 1.2 Create `.env.example` at repository root
- [x] 1.3 Create `README.md` at repository root with setup instructions

## 2. Backend (FastAPI)

- [x] 2.1 Create `backend/app/main.py` with FastAPI app and `GET /health` endpoint
- [x] 2.2 Create `backend/requirements.txt` with fastapi, uvicorn[standard], pydantic-settings
- [x] 2.3 Create `backend/Dockerfile`

## 3. Frontend (Vue 3 + Vuetify)

- [x] 3.1 Initialize Vue 3 + TypeScript + Vite project in `frontend/`
- [x] 3.2 Install and configure Vuetify 3 plugin
- [x] 3.3 Create basic layout with AppBar and Hello World content
- [x] 3.4 Create `frontend/Dockerfile`

## 4. Docker Compose

- [x] 4.1 Create `docker-compose.yml` with backend and frontend services
- [x] 4.2 Verify both services start with `docker compose up` (requires Docker)

## 5. Verification

- [x] 5.1 Backend health endpoint returns 200 with `{"status": "ok"}`
- [x] 5.2 Frontend builds without TypeScript errors
- [ ] 5.3 Docker Compose starts both services successfully
