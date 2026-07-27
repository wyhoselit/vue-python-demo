## Why
Frontend login returns 401 when calling `/api/v1/users/me` after successful authentication. The JWT cookie is not being sent with the XHR request because the frontend Axios instance lacks `withCredentials: true`, and/or the CORS configuration doesn't allow credentials.

## What Changes
- Add `withCredentials: true` to Axios instance in `frontend/src/composables/useApi.ts`
- Verify CORS configuration allows credentials (`allow_credentials=True`, specific origin not `*`)
- Test end-to-end login → fetch user profile flow

## Capabilities

### New Capabilities
- `frontend-auth-cookie`: Ensure HttpOnly JWT cookie is sent with cross-origin requests

### Modified Capabilities
- `user-profile`: Frontend now properly retrieves user profile after login

## Impact
- `frontend/src/composables/useApi.ts`: Add `withCredentials: true`
- `backend/app/main.py`: Verify CORS `allow_credentials=True` and explicit origin