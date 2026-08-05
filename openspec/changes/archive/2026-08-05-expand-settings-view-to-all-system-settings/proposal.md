## Why

The current `SettingsView.vue` only supports a limited set of system settings (`tracing.admin` and `system.logfile_path`) and requires module-specific endpoints for management. This creates management overhead and makes it difficult to add new system settings efficiently. Currently, the frontend makes direct API calls to multiple module-specific endpoints, leading to fragmented code and increased maintenance burden.

## What Changes

- Create a centralized system configuration API (`/api/v1/system/config`) that supports bulk fetch of all system settings
- Implement a dynamic form component in `SettingsView.vue` that renders form controls based on the JSON content of each system setting
- Update `SettingsView.vue` to fetch all settings dynamically instead of individual key calls
- Provide frontend logic to dynamically save setting changes back to the backend
- Consolidate all dynamic setting management under a unified API interface

## Capabilities

### New Capabilities
- `system-config-management`: Comprehensive management of all system settings via a unified, dynamic interface

### Modified Capabilities
- `frontend-settings-view`: Enhanced from limited settings management to comprehensive dynamic settings panel with dynamic form rendering

## Impact

- Frontend: `SettingsView.vue` - Expanded from limited settings management to comprehensive dynamic settings panel
- Backend: System module API and setting service - Expanded scope to support unified configuration management
- Database: No schema change, utilizing existing `system_settings` table
- Developer Experience: Reduced maintenance overhead and easier addition of new system settings
