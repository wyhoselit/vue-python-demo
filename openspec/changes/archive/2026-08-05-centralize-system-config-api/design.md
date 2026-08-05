## Context

Currently, system-wide configuration parameters (like tracing settings and logfile path) are managed by individual modules, resulting in scattered API endpoints, duplicated logic for setting retrieval, and a fragmented frontend integration path.

## Goals / Non-Goals

**Goals:**
- Create a centralized system configuration API (`/api/v1/system/config`).
- Consolidate dynamic setting management for the entire application, including tracing settings and logfile path configuration.
- Improve API consistency for frontend integration.

**Non-Goals:**
- Migrate environment variable-based static configuration (Pydantic `Settings`) to the database (these remain in `core/config.py`).

## Decisions

- **Centralized API**: Consolidate all dynamic settings under `/api/v1/system/config`.
- **Database Storage**: Continue using the `system_settings` table, leveraging its JSON column for flexible value storage.
- **Route Refactoring**: Maintain backward compatibility for `/api/v1/admin/tracing/config` by redirecting its logic to the unified `setting_service` and `system/config` endpoint structure, while marking it for eventual migration.
- **Logfile Path Configuration**: Store logfile path under the `system.logfile_path` key in `system_settings`, allowing dynamic reconfiguration of the application's logfile destination.

## Risks / Trade-offs

- **API Compatibility**: The current admin tracing API will be refactored to delegate to new services, which could introduce subtle bugs in existing admin routes. → Rigorous unit testing on migrated endpoints.

## Front-end Integration

- **Unified Configuration API**: Frontend components should transition to making requests directly to `/api/v1/system/config/{key}` instead of module-specific endpoints (e.g., `/api/v1/admin/tracing/config`) for dynamic setting management. This provides a consistent, global path for system configurations.
