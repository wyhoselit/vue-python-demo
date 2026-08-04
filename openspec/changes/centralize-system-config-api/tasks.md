## 1. New Centralized API Implementation

- [x] 1.1 Create system module API file (`app/modules/system/api/config.py`)
- [x] 1.2 Implement GET `/api/v1/system/config/{key}` endpoint (list all settings)
- [x] 1.3 Implement PUT `/api/v1/system/config/{key}` endpoint (update settings)
- [x] 1.4 Add comprehensive test cases for all functions in `config.py` (CRUD, validation, edge cases)
- [x] 1.5 Test new endpoint with key-value scenarios

## 2. Trace Configuration Migration

- [x] 2.1 Update `admin/api/tracing.py` to delegate tracing config to system service
- [x] 2.2 Create shared utility methods between admin and system APIs
- [x] 2.3 Ensure backward compatibility for existing admin routes
- [x] 2.4 Add test cases for tracing endpoint covering the refactored delegation logic
- [x] 2.5 Clean up legacy test cases for tracing API that no longer apply post-refactor

## 3. Integration and Deployment

- [x] 3.1 Update project routing configuration (e.g., `app/api/v1/router.py`)
- [x] 3.2 Add testing coverage for new and migrated endpoints
- [x] 3.3 Prepare frontend integration documentation

## 4. Extended Configuration Management

- [x] 4.1 Implement `system.logfile_path` configuration to support dynamic logfile path management
- [x] 4.2 Add GET `/api/v1/system/config/system.logfile_path` endpoint for retrieving logfile path
- [x] 4.3 Add PUT `/api/v1/system/config/system.logfile_path` endpoint for updating logfile path
- [x] 4.4 Add comprehensive test cases for logfile path configuration
- [x] 4.5 Update frontend endpoints to call system-config API for configuration management
- [x] 4.6 Update frontend components to use centralized system-config API endpoints
- [x] 4.7 Add frontend tests for new logfile path configuration endpoints
- [x] 4.8 Prepare documentation for extended configuration management