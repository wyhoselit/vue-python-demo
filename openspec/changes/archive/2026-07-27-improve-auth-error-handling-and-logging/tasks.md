## 1. Backend Logging & Exceptions

- [x] 1.1 Add `python-json-logger` dependency
- [x] 1.2 Create `backend/app/core/logging.py` with JSON formatter
- [x] 1.3 Add request ID middleware
- [x] 1.4 Create `backend/app/core/exceptions.py` with AuthException hierarchy
- [x] 1.5 Add global exception handler in `main.py`

## 2. Auth Endpoint Updates

- [x] 2.1 Refactor `/register` to raise `EmailAlreadyExistsError`
- [x] 2.2 Refactor `/login` to raise `InvalidCredentialsError`
- [x] 2.3 Add request ID to response headers (X-Request-ID)

## 3. Frontend Integration

- [x] 3.1 Update `frontend/src/services/auth.ts` to parse unified error response
- [x] 3.2 Update `frontend/src/stores/auth.ts` to expose typed errors
- [x] 3.3 Update `LoginForm.vue` / `RegistrationForm.vue` to show specific messages

## 4. Testing

- [x] 4.1 Backend tests: verify error codes and log output
- [x] 4.2 Frontend tests: verify error display logic