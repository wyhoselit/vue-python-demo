## Why

The admin page currently shows all sections (System Info, Tracing Config, Logs) on a single long page. Users requested separate, dedicated pages for each section with cleaner navigation and better information architecture.

## What Changes

- Split `/admin` route into separate routes: `/admin/info`, `/admin/logs`, `/admin/settings`
- Create modular Vue components for each admin section
- Add navigation sidebar to admin layout
- Keep `/admin` as a redirect to `/admin/info`

## Capabilities

### New Capabilities
- `admin-info-page`: Dedicated system information display page
- `admin-logs-page`: Dedicated logs viewer page with filtering
- `admin-settings-page`: Dedicated settings management page with tracing controls
- `admin-navigation`: Sidebar navigation component for admin section

### Modified Capabilities

## Impact

- `frontend/src/router/index.ts` - Add new routes
- `frontend/src/modules/admin/views/AdminStatus.vue` - Refactor into separate components
- `frontend/src/modules/admin/views/SystemInfo.vue` - New component
- `frontend/src/modules/admin/views/LogsView.vue` - New component
- `frontend/src/modules/admin/views/SettingsView.vue` - New component