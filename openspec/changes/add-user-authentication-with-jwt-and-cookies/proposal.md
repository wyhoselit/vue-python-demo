## Why

The backend currently lacks a standardized, secure user authentication mechanism. Relying on mock data for users prevents secure session management, registration, and user-specific data isolation. Implementing JWT-based authentication with HttpOnly cookies will provide a secure and scalable way to manage user sessions and protect API resources.

## What Changes

- Implement User registration (hashing passwords, storing in DB).
- Implement User login (validating credentials, signing JWTs).
- Implement secure JWT-based authentication.
- Introduce HttpOnly Cookie storage for JWTs.
- Create frontend AuthContext to manage user state.
- Protect dashboard and API routes requiring auth.
- **BREAKING**: API endpoints for users/dashboard now require a valid JWT.

## Capabilities

### New Capabilities
- `user-auth`: Automated registration, login, JWT issuance, and cookie-based authentication management.

### Modified Capabilities
- `backend-api`: Requires secure authentication for protected endpoints.
- `frontend-dashboard`: Requires authorized user session to view dashboard data.

## Impact

- `backend/app/api/v1/auth`: New endpoints for register and login.
- `backend/app/core/security.py`: Logic for JWT generation, password hashing, and token verification.
- `backend/app/models/user.py`: New database model.
- `frontend/src/composables/useApi.ts`: Updated to include Authorization/Cookie management.
- `frontend/src/services/auth.ts`: New service for login/register/logout.
- `frontend/src/stores/auth.ts`: New Pinia store for user session management.
