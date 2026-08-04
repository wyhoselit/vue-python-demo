## Context

The current authentication system in `/backend/app/api/v1/deps.py` uses cookie-based authentication:

```python
def get_current_user(request: Request, db: Session = Depends(get_db)):
    token = request.cookies.get("access_token")
    ...
```

This works for browser-based clients, but modern API consumers prefer Bearer token authentication via the Authorization header, which is the standard for REST APIs.

## Goals / Non-Goals

**Goals:**
- Add support for `Authorization: Bearer <token>` header authentication
- Maintain backward compatibility with existing cookie-based authentication
- Keep admin privilege requirements for system configuration endpoints
- No database or model changes required

**Non-Goals:**
- Add token refresh functionality
- Create new authentication endpoints
- Change password hashing or token expiration logic
- Modify the existing SystemSetting model or migrations

## Decisions

**Decision 1: Header Precedence**
- If Authorization header is present, use it
- Fallback to cookie if header not present
- Rationale: Allows explicit opt-in to header auth while preserving existing behavior

**Decision 2: Minimal Code Changes**
- Modify `get_current_user()` to extract token from multiple sources
- Create a helper function `extract_token_from_request()` to keep logic clean
- Rationale: Single responsibility, easy to test, minimal surface area for bugs

**Decision 3: Standard Bearer Format**
- Follow RFC 6750 (OAuth 2.0 Bearer Token Usage)
- Parse Authorization header as `Bearer <token>`
- Rationale: Industry standard, well-understood by developers

**Decision 4: Admin Access to Tracing Config**
- Default tracing configuration (e.g., `system.tracing`) shall be accessible for reading and updates via the config API by admin users.
- Rationale: Enables centralized management of administrative system configurations.

**Decision 5: Default Bearer Token Storage**
- Default bearer tokens SHALL be stored in the system configuration key `system.default_bearer_token`.
- Rationale: Centralizes token management, allows administrators to set/modify tokens without code changes, provides single source of truth for default authentication.

**Decision 6: Default System Config Values**
- The following system configuration keys exist with default values:
  - `tracing.admin = false` (admin access to tracing system)
  - `system.default_bearer_token = ""` (empty default token - admin must set)
  - `system.auth_method = "cookie_or_bearer"` (auth method preference)
  - `system.token_expiry_hours = 24` (token expiration time)
- Rationale: Provides predictable configuration state, enables authentication flexibility, supports administrative control over system behavior.

## Risks / Trade-offs

[Risk] Token parsing edge cases (malformed header, missing "Bearer" prefix) → Mitigation: Use standard `OAuth2PasswordBearer` dependency or custom robust parsing
[Risk] Security concern - token in header vs cookie → Mitigation: Both methods use same token verification logic; no additional security risk
[Risk] Breaking change if header parsing fails → Mitigation: Proper fallback to cookie auth

## Migration Plan

1. Update `get_current_user()` to check Authorization header first
2. Add unit tests for new auth flow
3. Update API documentation to indicate Bearer token support
4. Deploy to staging for verification
5. No rollback needed - changes are backward compatible

## Open Questions

- Should we remove cookie auth in a future major version?
- Do we need to add this to OpenAPI/Swagger documentation?
- Should we log which auth method was used (header vs cookie)?