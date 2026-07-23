## 1. Backend Testing Setup (Pytest)

- [x] 1.1 Add `pytest`, `httpx`, `pytest-asyncio` to `backend/requirements.txt`.
- [x] 1.2 Create `backend/tests/__init__.py`.
- [x] 1.3 Create `backend/tests/conftest.py` with test client and test database fixtures (using SQLite in-memory for speed).
- [x] 1.4 Configure `pytest.ini` in `backend/` for test discovery and reporting.

## 2. Backend Test Cases

- [x] 2.1 Create `backend/tests/test_config.py` for `app.core.config` tests.
- [x] 2.2 Create `backend/tests/test_database.py` for `app.core.database` tests (basic connection, session yielding).
- [x] 2.3 Create `backend/tests/test_api_health.py` for `/health` and `/api/v1/health` endpoint tests.
- [x] 2.4 Create `backend/tests/test_api_cors.py` for CORS headers verification.
- [x] 2.5 Create `backend/tests/test_api_errors.py` for global exception handlers.

## 3. Frontend Testing Setup (Vitest)

- [x] 3.1 Add `vitest`, `@vue/test-utils`, `happy-dom` to `frontend/package.json` devDependencies.
- [x] 3.2 Create `frontend/vitest.config.ts` for Vitest configuration.
- [x] 3.3 Create `frontend/src/__tests__/__init__.ts` (or equivalent).
- [x] 3.4 Add `test` script to `frontend/package.json`: `vitest --run`.

## 4. Frontend Test Cases

- [x] 4.1 Create `frontend/src/__tests__/components/App.spec.ts` for App component rendering.
- [x] 4.2 Create `frontend/src/__tests__/components/Layout.spec.ts` for Layout component rendering.
- [x] 4.3 Create `frontend/src/__tests__/stores/theme.spec.ts` for Pinia theme store.
- [x] 4.4 Create `frontend/src/__tests__/router/index.spec.ts` for basic router navigation.
- [x] 4.5 Create `frontend/src/__tests__/services/api.spec.ts` for mocked API service calls.

## 5. Documentation and CI Integration

- [x] 5.1 Update `README.md`: Add "How to run tests" section with commands for backend and frontend.
- [x] 5.2 (Optional) Update `backend/Dockerfile` to include a test stage.
- [x] 5.3 (Optional) Update `frontend/Dockerfile` to include a test stage.
- [x] 5.4 (Optional) Update `docker-compose.yml` to run tests as a separate service or in CI.
- [x] 5.5 Add a root-level `test` or `ci-test` script to run both backend and frontend tests.

## 6. Verification

- [x] 6.1 Run `cd backend && pip install -r requirements.txt` (if not done by Dockerfile).
- [x] 6.2 Run `cd backend && pytest` and verify all backend tests pass.
- [x] 6.3 Run `cd frontend && npm install` (if not done by Dockerfile).
- [x] 6.4 Run `cd frontend && npm run test` and verify all frontend tests pass.
- [x] 6.5 Run the combined CI test command from root and verify both pass.
