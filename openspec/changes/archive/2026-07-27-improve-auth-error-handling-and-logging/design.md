## Context
- Auth endpoints currently return minimal error info.
- No logging for audit/troubleshooting.

## Goals / Non-Goals
**Goals:**
- Structured JSON logging with request ID propagation.
- Custom exception classes mapped to HTTP status codes.
- Unified error response format across auth endpoints.
- Frontend displays specific user-friendly messages.

**Non-Goals:**
- Internationalization (i18n) of error messages.
- Rate limiting logic (separate concern).

## Decisions
1. **Logging Library**: Use Python stdlib `logging` with `python-json-logger` for JSON output.
2. **Request ID**: Generate UUID per request via middleware.
3. **Exception Base**: `AuthException(status_code, error_code, detail)` subclasses for each error.
4. **Middleware**: Global exception handler converts exceptions to unified JSON response.
5. **Frontend**: Update `authService` to parse error response and expose `error_code` + `detail`.

## Risks / Trade-offs
- Adding `python-json-logger` dependency.
- Must ensure request ID is available in all log contexts.