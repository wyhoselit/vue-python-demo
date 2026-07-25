# Frontend API Service Specification

## Purpose
Defines the Axios-based API service wrapper for frontend-backend communication.

## Requirements

### Requirement: API Service Module
The system SHALL provide an API service module (`frontend/src/services/api.ts`).

#### Scenario: Axios instance configured
- **WHEN** `frontend/src/services/api.ts` is imported
- **THEN** it SHALL export an Axios instance configured with:
  - Base URL from environment (`import.meta.env.VITE_API_BASE_URL` or `/api`)
  - Request/response interceptors for auth tokens
  - Error handling interceptor

### Requirement: useApi Composable
The system SHALL provide a `useApi` composable (`frontend/src/composables/useApi.ts`) for component-level API calls.

#### Scenario: Composable provides standard methods
- **WHEN** `useApi()` is called
- **THEN** it SHALL return an object with:
  - `get(url, params?)`
  - `post(url, data?)`
  - `put(url, data?)`
  - `patch(url, data?)`
  - `delete(url)`
  - `request(config)`

### Requirement: Error handling
The API service SHALL handle common error scenarios.

#### Scenario: Network errors caught
- **WHEN** Axios request fails due to network error
- **THEN** service SHALL return a standardized error object.

#### Scenario: HTTP errors handled
- **WHEN** backend returns 4xx/5xx status
- **THEN** service SHALL throw/return error with status and message.

#### Scenario: Authentication errors trigger logout
- **WHEN** 401 Unauthorized is received
- **THEN** auth store SHALL be notified to clear user state.

### Requirement: Request/Response interceptors
The API service SHALL use interceptors for common functionality.

#### Scenario: Auth token attached to requests
- **WHEN** request is made and user is authenticated
- **THEN** Authorization header SHALL be attached with Bearer token.

#### Scenario: Response normalized
- **WHEN** response is received
- **THEN** service SHALL return `response.data` directly.

### Requirement: TypeScript types
API service SHALL use TypeScript interfaces for request/response types.

#### Scenario: Types exported
- **WHEN** importing from `frontend/src/services/api.ts`
- **THEN** TypeScript types SHALL be available for:
  - API response wrapper
  - Common request payloads
  - Error response structure