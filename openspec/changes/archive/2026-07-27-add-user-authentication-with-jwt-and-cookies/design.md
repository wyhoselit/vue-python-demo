## Context
- Current authentication is non-existent.
- Need a reliable system for user session management in FastAPI and Vue.js.

## Goals / Non-Goals
**Goals:**
- Secure JWT-based auth with HttpOnly cookies.
- Password hashing using `passlib` (bcrypt).
- Consistent session state across frontend and backend.

**Non-Goals:**
- Social login (OAuth2/OIDC) for now.
- Password reset/email verification in initial scope.

## Decisions
1. **JWT Strategy**: Stateless JWT stored in HttpOnly, SameSite=Strict cookies to prevent XSS.
2. **Password Hashing**: `passlib[bcrypt]` for secure password storage.
3. **Session Management**: Frontend Pinia store for session state, Axios interceptors for handling auth headers/cookies.

## Risks / Trade-offs
- [Cookie Security] → Mitigation: Set Secure, HttpOnly, and SameSite=Strict flags.
- [Token Expiration] → Mitigation: Implement refresh token mechanism if needed, start with short-lived JWT.
