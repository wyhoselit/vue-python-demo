# Proposal: Improve Auth Error Handling and Logging

## Why
- Currently, auth errors return generic "Registration failed" or status codes without context.
- Hard to debug issues in production without backend logging.
- Frontend lacks actionable error details for users.

## What
- Implement structured logging in FastAPI.
- Create custom exception handling.
- Unified error response format.

## Scope
- `backend/app/core/logging.py`, `backend/app/core/middleware.py`, `backend/app/core/exceptions.py`
- `backend/app/main.py`
- `backend/app/api/v1/endpoints/auth.py`
- `frontend/src/services/auth.ts`, `frontend/src/stores/auth.ts`
- `frontend/src/views/LoginForm.vue`, `frontend/src/views/RegistrationForm.vue`
