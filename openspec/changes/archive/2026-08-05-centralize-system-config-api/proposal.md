## Why

System configurations (such as admin tracing toggle and logfile path) are currently scattered across module-specific APIs like `/api/v1/admin/tracing/config`. This makes it difficult for frontend applications to fetch and manage dynamic settings globally. Exposing settings via a centralized `system/config` API endpoint in the `system` module improves developer experience and consolidates configuration endpoints.

## What Changes

- Introduce a new endpoint `/api/v1/system/config` in the system module to retrieve and update configurations.
- Refactor the tracing and logfile config logic, moving it from the `admin` API module to the `system` API module.
- Retain the `/api/v1/admin/tracing/config` endpoint route mapping but delegate its business logic execution directly to the new central settings management.

## Capabilities

### New Capabilities
- `system-config-api`: Provides a centralized `/api/v1/system/config` endpoint for reading and writing dynamic configurations (including tracing and logfile path) from the `system_settings` database.

### Modified Capabilities
- `system-settings`: Exposes database configuration items via dynamic interfaces, bridging DB records and API endpoints.

## Impact

- **Backend API**: New route file `app/modules/system/api/config.py`. Updated `app/modules/admin/api/tracing.py` to route requests dynamically.
- **Frontend Integration**: UI setting changes will make unified requests to `system/config` instead of module-specific endpoints.
