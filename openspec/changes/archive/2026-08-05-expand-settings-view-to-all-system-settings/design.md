## Context
The current configuration management is scattered, with frontend components making direct module-specific API calls. We aim to consolidate this by exposing a bulk endpoint for all system settings and enabling dynamic frontend rendering.

## Goals / Non-Goals
**Goals:**
- Provide a bulk API endpoint `/api/v1/system/config` to fetch all system settings.
- Implement a dynamic UI in SettingsView.vue that renders settings based on their data type.
- Provide comprehensive frontend form controls for all system setting types (boolean, string, number, JSON).

**Non-Goals:**
- Migration of static configuration from `core/config.py` to the database.

## Decisions
- **Bulk API Endpoint**: Add `GET /api/v1/system/config` that returns all `SystemSetting` records as a JSON map. Use `setting_service.get_all_settings()` for backend implementation.
- **Dynamic Frontend Form**: Use Vue components to map setting types (boolean, string, number) to appropriate input elements (checkbox, text input, number input). Implement a SettingsConfig component that receives the settings map and generates the appropriate form controls dynamically.
- **Backend Service Update**: Update `setting_service.py` to support retrieving all settings at once.
- **Frontend Integration**: Create a SettingsConfig component in SettingsView.vue that accepts the settings data and dynamically renders form controls.

## Risks / Trade-offs
- **Backend Performance**: Fetching all settings at once might impact performance if the number of settings grows significantly. → Mitigation: Add basic pagination if necessary, though current settings are small.
- **Frontend Performance**: Dynamic rendering of many settings might impact UI performance → Mitigation: Implement lazy loading for many settings, virtual scrolling if needed.
- **Type Safety**: Different setting types require proper validation → Mitigation: Create a Setting interface with type guards and proper typing for the settings map.

## Implementation Architecture
The system will consist of:
1. **Backend**: New bulk endpoint `GET /api/v1/system/config` using `setting_service.get_all_settings()` to return settings map.
2. **Frontend**: Dynamic SettingsConfig component that renders controls based on setting type.
3. **API Layer**: Unified endpoint for all settings operations with backward compatibility.
4. **Service Layer**: Enhanced `setting_service.py` with bulk retrieval capabilities.