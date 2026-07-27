## Why
The backend `/api/v1/users/me` endpoint is missing, causing a 404 error on the frontend when attempting to retrieve the current user's profile.

## What Changes
- Implement `/api/v1/users/me` endpoint in the backend.
- **BREAKING**: None.

## Capabilities

### New Capabilities
- `user-profile`: Retrieve the currently authenticated user's profile information.

### Modified Capabilities
- `users`: Expose current user endpoint in addition to existing list endpoint.

## Impact
- `backend/app/api/v1/endpoints/users.py`: Add `get_me` endpoint.
- `frontend/src/services/auth.ts`: Ensure service correctly handles the new endpoint.