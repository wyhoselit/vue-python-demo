## 1. Setup

- [x] 1.1 Modify /backend/app/api/v1/deps.py to support Bearer token authentication
- [x] 1.2 Update imports and helper function for token extraction
- [x] 1.3 Add unit test file for new authentication logic

## 2. Core Implementation

- [x] 2.1 Update get_current_user() to check Authorization header before cookie
- [x] 2.2 Implement extract_token_from_request() helper function
- [x] 2.3 Parse Bearer token format and validate token
- [x] 2.4 Maintain backward compatibility with cookie auth
- [x] 2.5 Update existing tests for new auth flow

## 3. Testing & Validation

- [x] 3.1 Write unit tests for get_current_user() with Bearer tokens
- [x] 3.2 Test token parsing edge cases (malformed header, missing Bearer prefix)
- [x] 3.3 Validate unauthenticated requests return proper error responses
- [x] 3.4 Test cookie auth fallback works correctly
- [x] 3.5 Add integration tests for system config API with Bearer tokens

## 4. Default Bearer Token Handling
- [x] 4.1 Create `.token` file in project root if not exists
- [x] 4.2 Update system config API to read/write `system.default_bearer_token` from/to `.token` file
- [x] 4.3 Add db migration/initialization script to read `.token` and seed `system.default_bearer_token`
- [x] 4.4 Write unit tests for `.token` file read/write operations
- [x] 4.5 Add integration test for system initialization with `.token` file
