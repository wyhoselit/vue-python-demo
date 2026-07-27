## Context
- Backend sets HttpOnly JWT cookie on login (`/api/v1/auth/login`)
- Frontend calls `/api/v1/users/me` after login but gets 401
- Cookie is not sent because `withCredentials: false` (default) in Axios
- CORS must allow credentials with explicit origin (not `*`)

## Goals / Non-Goals
**Goals:**
- Send HttpOnly JWT cookie with cross-origin XHR requests
- Verify CORS allows credentials with specific origin

**Non-Goals:**
- Change JWT storage mechanism (keep HttpOnly cookie)
- Add refresh token logic

## Decisions
1. **Axios `withCredentials: true`**: Add to `useApi.ts` Axios instance creation. This is the standard way to send cookies with cross-origin requests.
2. **CORS Configuration**: Backend already has `allow_credentials=True` and explicit `allow_origins=["http://localhost:5173"]`. No change needed if config is correct.
3. **Cookie Settings**: Keep `HttpOnly`, `Secure`, `SameSite=Strict` (already set in auth endpoint)

## Risks / Trade-offs
- [CORS with credentials requires explicit origin] → Mitigation: Ensure `allow_origins` includes frontend URL, not wildcard
- [Secure cookie requires HTTPS in production] → Mitigation: Only affects local dev (HTTP), production uses HTTPS