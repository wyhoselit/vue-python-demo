## Why

Currently, the system configuration API (`/api/v1/system/config/{key}`) only supports authentication via `access_token` cookies. Modern frontend applications and API consumers often prefer or require Bearer token authentication via the Authorization header. Adding support for Authorization: Bearer tokens will improve API flexibility and compatibility with standard authentication patterns.

## What Changes

- Update authentication dependencies in `/app/api/v1/deps.py` to accept both cookie-based and Bearer token authentication for system config endpoints
- Modify the `get_current_user` function to check for `access_token` in both cookies and Authorization header (Bearer format)
- No breaking changes to existing functionality - cookie auth continues to work
- Maintains admin privilege requirement for system config access
- Admin users can view and update tracing configuration (e.g., `tracing.admin`) via config API
- Support creating/updating default tokens via config API
- Default bearer token stored in `system.default_bearer_token` config key
- Default system config values documented for administration

## Capabilities

### New Capabilities
- `bearer-auth-support`: Adds support for Authorization: Bearer token authentication to system configuration API endpoints
- `admin-config-management`: Admin users can read and update system configuration including tracing settings
- `default-token-management`: Default bearer token can be stored and managed via config API

### Modified Capabilities
- `system-config-api`: Modifies authentication requirements to accept both cookie and Bearer token auth methods; adds admin access to tracing config

## Impact

- Affected file: `/app/api/v1/deps.py` (authentication logic)
- API endpoints: `/api/v1/system/config/{key}` (GET and PUT)
- No database or model changes required
- Backward compatible - existing cookie-based auth continues to work
- Frontend and external API consumers can now use standard Bearer token auth

## Default System Configuration

The system provides the following default configuration values:

| Key | Default Value | Description |
|-----|---------------|-------------|
| `system.tracing` | `false` | Admin access to tracing system |
| `system.default_bearer_token` | `""` | Default bearer token (empty - admin must set) |
| `system.auth_method` | `"cookie_or_bearer"` | Authentication method preference |
| `system.token_expiry_hours` | `24` | Token expiration time in hours |