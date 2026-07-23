## Context

The current monorepo (FastAPI backend, Vue frontend) lacks automated tests. This makes refactoring risky, introduces potential regressions, and slows down development velocity. Both applications have basic functionality but no assurances of correctness beyond manual checks.

## Goals / Non-Goals

**Goals:**
- Establish robust testing frameworks for both backend and frontend.
- Implement foundational tests for core functionalities:
    - Backend: API endpoints (health), configuration loading, database connection.
    - Frontend: Component rendering, state management (Pinia), router navigation, API service interaction.
- Provide clear instructions for running tests in development and CI environments.
- Ensure tests run independently (e.g., test DB for backend, mocking for frontend API calls).

**Non-Goals:**
- Achieve 100% test coverage for all code. Initial focus is on core functionalities.
- Implement end-to-end (E2E) tests.
- Optimise test performance (initial setup over speed).
- Introduce complex test data seeding/factories beyond basic needs.

## Decisions

### 1. Backend Testing Framework: Pytest
**Choice:** `pytest`, `httpx` (for API calls), `pytest-asyncio` (for async tests).
**Rationale:** `pytest` is the de facto standard for Python testing, highly flexible and extensible. `httpx` is a modern, async-friendly HTTP client suitable for testing FastAPI. `pytest-asyncio` simplifies testing async functions.
**Alternatives:** `unittest` (more boilerplate), `nose2` (less popular).

### 2. Backend Test Database Strategy: SQLite in-memory or file-based
**Choice:** For most tests, use an in-memory SQLite database. For integration tests that need persistence or specific features, use a file-based SQLite database.
**Rationale:** Fast and isolated test runs. Avoids reliance on external PostgreSQL instance during testing.
**Alternatives:** Dockerized PostgreSQL for tests (adds setup complexity), mock SQLAlchemy engine (limits realism).

### 3. Frontend Testing Framework: Vitest
**Choice:** `Vitest` with `@vue/test-utils` and `happy-dom`.
**Rationale:** `Vitest` is a fast, Vite-native test runner, offering excellent developer experience for Vue projects. `@vue/test-utils` is the official library for mounting and interacting with Vue components. `happy-dom` provides a lightweight, fast DOM environment without a real browser.
**Alternatives:** `Jest` (more configuration needed for Vite), `Karma`/`Mocha` (browser-based, slower).

### 4. Frontend API Mocking: Mock Service Worker (MSW) or simple mocks
**Choice:** Simple manual mocking of API service calls using `vitest.mock()` for unit/component tests.
**Rationale:** Reduces complexity for initial test setup. MSW can be overkill for smaller projects unless complex network mocking is strictly required.
**Alternatives:** `Mock Service Worker` (more powerful, but heavier for initial setup).

### 5. Test Integration in CI
**Choice:** Provide simple `npm run test` and `pytest` commands. Dockerfile/docker-compose integration will be optional, with documentation provided.
**Rationale:** Keeps the initial implementation focused on writing tests rather than complex CI pipelines. Users can adapt the commands to their CI system.
**Alternatives:** Fully integrate testing stages into Dockerfiles with multi-stage builds (more complex initial setup).

## Risks / Trade-offs

| Risk | Mitigation |
|------|------------|
| Test setup complexity for database | Use fixtures for database session management (`pytest-alembic` or custom fixture). Document clearly. |
| Frontend tests become flaky due to async rendering | Use `await nextTick()` and `flushPromises()` as needed with `@vue/test-utils`. |
| API mocking not realistic enough | Ensure mock responses cover critical paths and error cases. Extend with `MSW` if fidelity becomes an issue. |
| Performance of tests on large codebase | Focus on unit tests where possible. Introduce component/integration tests selectively. Optimize later. |

## Migration Plan

1. Install backend test dependencies (pytest, httpx, pytest-asyncio).
2. Create `backend/tests/` directory and basic `conftest.py` with app and test DB fixtures.
3. Write backend tests (health, config, database, API).
4. Install frontend test dependencies (vitest, @vue/test-utils, happy-dom).
5. Configure `vitest.config.ts` and `package.json`.
6. Create `frontend/src/__tests__/` and write frontend tests.
7. Update `README.md` with instructions for running tests.
8. (Optional) Add CI stages to Dockerfiles/docker-compose.

**Rollback:** Remove test files, dependencies, and documentation. No impact on application logic.
