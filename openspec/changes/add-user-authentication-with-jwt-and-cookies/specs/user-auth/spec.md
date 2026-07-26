## ADDED Requirements

### Requirement: User Registration
The system SHALL allow new users to register with an email and password, creating a secure account.

#### Scenario: Successful registration
- **WHEN** a client POSTs to `/api/v1/auth/register` with a valid email and password
- **THEN** a new User record is created with a hashed password
- **AND** a 201 response is returned with the created user's public info (id, email)

#### Scenario: Duplicate email registration fails
- **WHEN** a client attempts to register with an already registered email
- **THEN** a 400 response is returned with an error message

### Requirement: User Login
The system SHALL authenticate registered users and issue a JWT stored in an HttpOnly cookie.

#### Scenario: Successful login
- **WHEN** a client POSTs to `/api/v1/auth/login` with correct email and password
- **THEN** a 200 response is returned
- **AND** a `Set-Cookie` header sets an HttpOnly, Secure, SameSite=Strict cookie named `access_token` containing the JWT

#### Scenario: Failed login with wrong password
- **WHEN** a client provides an incorrect password
- **THEN** a 401 response is returned with an error message

#### Scenario: Failed login with non-existent email
- **WHEN** a client provides an email not in the database
- **THEN** a 401 response is returned with an error message

### Requirement: JWT Authentication Middleware
The system SHALL validate the JWT from the HttpOnly cookie on all protected endpoints.

#### Scenario: Valid token grants access
- **WHEN** a request includes a valid `access_token` cookie
- **THEN** the request proceeds and the current user is injected into the route handler

#### Scenario: Missing or invalid token denies access
- **WHEN** a request lacks a valid `access_token` cookie
- **THEN** a 401 response is returned

### Requirement: Protected User Endpoint
The system SHALL expose a `/api/v1/users/me` endpoint returning the current authenticated user's profile.

#### Scenario: Authenticated user gets profile
- **WHEN** an authenticated user GETs `/api/v1/users/me`
- **THEN** a 200 response returns the user's email and id

### Requirement: Frontend Authentication State
The frontend SHALL maintain a reactive authentication state (user, loading, error) via Pinia.

#### Scenario: Login updates state and navigates
- **WHEN** the user submits valid credentials in `LoginForm.vue`
- **THEN** the `authStore` updates with user data and the router navigates to `/dashboard`

#### Scenario: Logout clears state
- **WHEN** the user triggers logout
- **THEN** the `authStore` clears user data and the cookie is cleared

## MODIFIED Requirements

### Requirement: Backend API protection (from backend-api)
The system SHALL require authentication for all endpoints under `/api/v1/` except `/auth/*` and `/health`.

#### Scenario: Protected endpoint access
- **WHEN** an unauthenticated request targets a protected `/api/v1/` endpoint
- **THEN** a 401 response is returned

### Requirement: Dashboard Data Access (from frontend-dashboard)
The Dashboard view SHALL only render for authenticated users.

#### Scenario: Authenticated access
- **WHEN** an authenticated user navigates to `/dashboard`
- **THEN** the dashboard data is fetched and displayed

#### Scenario: Unauthenticated redirect
- **WHEN** an unauthenticated user navigates to `/dashboard`
- **THEN** they are redirected to `/login`