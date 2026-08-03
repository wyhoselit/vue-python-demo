## 1. Router Configuration

- [x] 1.1 Add new routes for /admin/info, /admin/logs, /admin/settings
- [x] 1.2 Add redirect from /admin to /admin/info

## 2. Component Creation

- [x] 2.1 Create SystemInfo.vue component
- [x] 2.2 Create LogsView.vue component
- [x] 2.3 Create SettingsView.vue component

## 3. Navigation

- [x] 3.1 Create AdminNavigation.vue sidebar component
- [x] 3.2 Update router-view structure to include navigation sidebar

## 4. API Integration

- [x] 4.1 Refactor API calls from AdminStatus.vue to shared endpoints
- [x] 4.2 Ensure all API endpoints work with new components

## 5. Testing & Cleanup

- [x] 5.1 Update tests for new routes and components
- [x] 5.2 Remove or deprecate AdminStatus.vue (keep temporarily with redirect)

## 6. Test Case Addition

- [x] 6.1 Add test cases for SystemInfo.vue
- [x] 6.2 Add test cases for LogsView.vue
- [x] 6.3 Add test cases for SettingsView.vue
- [x] 6.4 Add integration tests for new admin routes