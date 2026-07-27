## Context
- Current `/api/v1/users/me` endpoint returns 404.
- Frontend `authStore.fetchCurrentUser()` calls `GET /api/v1/users/me` expecting user profile.
- Existing user authentication uses JWT in HttpOnly cookie.

## Goals / Non-Goals
**Goals:**
- Add `GET /api/v1/users/me` endpoint returning current user's `id` and `email`.
- Reuse existing JWT verification middleware.

**Non-Goals:**
- Modify existing user list endpoint (`GET /api/v1/users`).
- Add new fields to User model.

## Decisions
1. **Endpoint location**: Add to `backend/app/api/v1/endpoints/users.py` alongside existing `GET /users`.
2. **Authentication**: Use existing `get_current_user` dependency (from security middleware) to inject user from JWT cookie.
3. **Response shape**: `{ "id": number, "email": string }` — matches frontend expectations.

## Risks / Trade-offs
- [Token validation failure] → Mitigation: Return 401 with error code `TOKEN_EXPIRED` or `INVALID_CREDENTIALS` (existing auth middleware handles this).
- [User deleted but token valid] → Mitigation: Return 401 if user not found in DB.