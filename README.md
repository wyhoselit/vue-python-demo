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
│   │   ├── api/          # API versioning (v1)
│   │   │   └── v1/
│   │   │       ├── endpoints/
│   │   │       │   ├── dashboard.py # Dashboard stats endpoint
│   │   │       │   └── users.py     # Users list endpoint
│   │   │       └── router.py    # Main API router
│   │   ├── core/         # Core application logic
│   │   │   ├── config.py
│   │   │   ├── database.py
│   │   │   └── security.py
│   │   └── main.py       # FastAPI application entry
│   ├── alembic/      # Alembic migration scripts
│   ├── requirements.txt
│   ├── Dockerfile
│   └── tests/        # Backend tests
├── frontend/         # Vue 3 + Vuetify frontend
│   ├── src/
│   │   ├── assets/
│   │   ├── components/
│   │   ├── composables/ # Reusable Vue functions (e.g., useApi)
│   │   ├── layouts/     # Application layouts (e.g., DefaultLayout)
│   │   ├── plugins/     # Vuetify, Pinia setup
│   │   ├── router/      # Vue Router configuration
│   │   ├── services/    # API service (axios)
│   │   ├── stores/      # Pinia stores (theme, auth)
│   │   └── views/       # Vue views (e.g., Dashboard.vue)
│   ├── package.json
│   ├── tsconfig.json
│   ├── vite.config.ts
│   ├── Dockerfile
│   └── src/__tests__/ # Frontend tests (Vitest)
├── docker-compose.yml
└── .env.example
```

## Local Development

### Backend

The FastAPI backend is structured for enterprise-grade scalability and maintainability.

**Architecture:**
- **Core Module (`app/core/`)**:
  - `config.py`: Centralized configuration using Pydantic Settings, loading environment variables from `.env`.
  - `database.py`: SQLAlchemy engine and session management for PostgreSQL/SQLite, with a FastAPI dependency for database sessions.
  - `security.py`: Stub for JWT token creation and verification (future use).
- **API Versioning (`app/api/v1/`)**:
  - Uses `APIRouter` for versioned endpoints, mounted at `/api/v1`.
  - Health check is available at `/api/v1/health` and legacy `/health`.
  - **New:** `GET /api/v1/dashboard/stats`: Returns platform statistics (Total Users, Active Sessions, API Calls).
  - **New:** `GET /api/v1/users`: Returns a list of mock user data.
- **Middleware**: Configured with CORS to allow frontend communication (e.g., from `http://localhost:5173`).
- **Error Handling**: Global exception handlers for `HTTPException` and unhandled exceptions provide consistent JSON responses.
- **Alembic**: Database migration tool configured to manage schema changes.

**Setup & Run:**

```bash
cd backend
# Create environment and install dependencies
uv sync
# Run development server
uv run uvicorn app.main:app --reload
```

**Alembic Migrations in Docker/Podman:**

Migrations are now automatically run on backend container startup.
- The `entrypoint.sh` script executes `alembic upgrade head` before starting the FastAPI application.
- This ensures the database schema is always up-to-date upon startup.
- To generate a new migration script (after model changes): `docker compose exec backend uv run alembic revision --autogenerate -m "Description"`

Backend runs at http://localhost:8000

**Environment Verification:**

```bash
# Verify uv installation
uv --version

# Verify backend environment
cd backend
uv run python --version
uv run pytest --version
```

### Frontend

The Vue 3 frontend leverages Vuetify for a modern UI.

**Architecture:**
- **Layouts (`src/layouts/`)**: `DefaultLayout.vue` provides the main app structure, integrating the `v-app-bar`, `v-navigation-drawer`, and `<router-view />`.
- **Stores (`src/stores/`)**: Pinia is used for state management, including `theme.ts` for dark/light mode persistence and `auth.ts` for user session.
- **API Integration (`src/composables/useApi.ts`)**: An Axios-based composable simplifies API calls, handles base URL configuration, and error interception.
- **Views (`src/views/`)**:
  - `Dashboard.vue`: Displays key metrics and user data fetched from backend APIs. Handles loading and error states.

**Setup & Run:**

```bash
cd frontend
npm install
npm run dev
```

Frontend runs at http://localhost:5173

### Running Tests

#### Backend Tests

```bash
cd backend
uv run pytest
```

#### Frontend Tests

```bash
cd frontend
npm run test
```

#### Run All Tests

```bash
# Run backend tests
cd backend && uv run pytest

# Run frontend tests
cd frontend && npm run test
```

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
- **New API Endpoints:**
  - `POST /api/v1/auth/register`: Register new user.
  - `POST /api/v1/auth/login`: Authenticate and set JWT cookie.
  - `GET /api/v1/users/me`: Returns current user profile.

## Frontend Layout Architecture

The frontend uses a layout component pattern for consistent UI:

### Layout Components

- `src/layouts/DefaultLayout.vue` - Main application layout with Vuetify navigation
  - Contains `<router-view />` for route content
  - Includes navigation drawer, app bar, and theme toggle

### App.vue Pattern

App.vue must use the layout wrapper:

```vue
<template>
  <DefaultLayout />
</template>

<script setup lang="ts">
import DefaultLayout from '@/layouts/DefaultLayout.vue'
</script>
```

**Do NOT** hardcode Vuetify components directly in App.vue - use layouts for consistent structure.

### Available Layouts

| Layout | Purpose |
|--------|---------|
| `DefaultLayout` | Main app with navigation drawer and theme toggle |

### Adding New Layouts

1. Create layout in `src/layouts/`
2. Export from `src/layouts/index.ts`
3. Update App.vue to use new layout
4. Run `npm run typecheck` to verify

### Pre-commit Check

A pre-commit hook verifies App.vue uses a layout component. Commit will fail if hardcoded content is detected.