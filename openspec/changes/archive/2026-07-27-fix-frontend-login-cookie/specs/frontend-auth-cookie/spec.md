## ADDED Requirements

### Requirement: Frontend Sends HttpOnly Cookie with Authenticated Requests
The frontend SHALL send the HttpOnly JWT cookie with all authenticated API requests.

#### Scenario: Login sets cookie and subsequent request includes it
- **WHEN** user successfully logs in via `/api/v1/auth/login`
- **THEN** response includes `Set-Cookie` header with `access_token`
- **AND** subsequent `GET /api/v1/users/me` request automatically includes the cookie
- **AND** server responds with 200 and user profile

#### Scenario: CORS preflight allows credentials
- **WHEN** browser sends OPTIONS preflight for authenticated request
- **THEN** response includes `Access-Control-Allow-Credentials: true`
- **AND** `Access-Control-Allow-Origin` matches frontend origin exactly

## MODIFIED Requirements

### Requirement: User Profile Retrieval (from user-profile)
The frontend SHALL successfully retrieve the current user's profile after login.

#### Scenario: Authenticated user retrieves profile
- **WHEN** user is logged in and navigates to dashboard
- **THEN** `authStore.fetchCurrentUser()` calls `GET /api/v1/users/me`
- **THEN** request includes `access_token` cookie automatically
- **THEN** `authStore` updates with user data (`id`, `email`)