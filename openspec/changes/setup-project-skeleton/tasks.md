## 1. Project Structure Setup

- [ ] 1.1 Create `backend/`, `frontend/`, `docker/` directories
- [ ] 1.2 Create `.env.example` at repository root
- [ ] 1.3 Create `README.md` at repository root with setup instructions

## 2. Backend (FastAPI)

- [ ] 2.1 Create `backend/app/main.py` with FastAPI app and `GET /health` endpoint
- [ ] 2.2 Create `backend/requirements.txt` with fastapi, uvicorn[standard], pydantic-settings
- [ ] 2.3 Create `backend/Dockerfile`

## 3. Frontend (Vue 3 + Vuetify)

- [ ] 3.1 Initialize Vue 3 + TypeScript + Vite project in `frontend/`
- [ ] 3.2 Install and configure Vuetify 3 plugin
- [ ] 3.3 Create basic layout with AppBar and Hello World content
- [ ] 3.4 Create `frontend/Dockerfile`

## 4. Docker Compose

- [ ] 4.1 Create `docker-compose.yml` with backend and frontend services
- [ ] 4.2 Verify both services start with `docker compose up`

## 5. Verification

- [ ] 5.1 Backend health endpoint returns 200 with `{"status": "ok"}`
- [ ] 5.2 Frontend builds without TypeScript errors
- [ ] 5.3 Docker Compose starts both services successfully
