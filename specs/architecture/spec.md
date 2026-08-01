# Project Architecture Specification

## 1. Directory Structure
- `modules/`: Contains business-specific logic (admin, user, system, dashboard, etc.).
- `shared/`: Contains infrastructure shared across 3+ business modules.
- `core/` (Backend): Contains application-level infrastructure, security, database settings.
- `tests/`: Business modules follow logic module structure.

## 2. Testing Alignment Rule
- Tests MUST reside in `modules/<module-name>/__tests__/` (Frontend) or `tests/modules/<module-name>/` (Backend).
- No flattened `tests/` directories unless for globally shared utilities.

## 3. Import Strategy
- Avoid relative paths across module boundaries.
- Favor aliased paths (e.g., `@/modules/admin/...`).