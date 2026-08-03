## Why

Currently, system settings like tracing are scattered across multiple tables (e.g., `trace_configurations`). This leads to schema proliferation and makes it harder to add new configuration options without creating new migrations each time.

A centralized `system_settings` table solves this, especially with SQLite's native JSON type for flexible storage.

## What Changes

- **New**: `SystemSetting` model in `backend/app/modules/system/models/system_setting.py`
- **New**: Alembic migration `xxx_create_system_settings_table.py`
- **New**: Refactored `TraceConfiguration` to use the new settings table (or deprecation)
- **Modified**: `TraceConfiguration` model and `get_tracing_config()` function

## Capabilities

### New Capabilities

- `system-settings`: A universal key-value store for all system configurations (JSON-based)
- `system-settings-migration`: Migration script to move existing config data
- `system-settings-api`: Helper functions for retrieving/storing settings

### Modified Capabilities

(None - this is a new capability)

## Impact

- **Files Affected**:
  - `backend/app/modules/admin/models/trace/trace_configuration.py` (refactor/ deprecate)
  - `backend/app/modules/core/database.py` (add new model import if needed)
  - `alembic/env.py` (may need to import new model for autogenerate)
- **Database**: New table `system_settings`
- **Dependencies**: None
- **APIs**: Internal change - `get_tracing_config()` signature may change