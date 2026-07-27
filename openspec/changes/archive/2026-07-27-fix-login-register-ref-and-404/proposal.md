# Proposal: Fix Login/Register Ref Error and 404 Routes

## Why
- `LoginForm.vue` uses `ref` without importing from `vue` → `ReferenceError`
- `/login` and `/register` routes return 404 in production (nginx serves static files, SPA fallback missing)
- Login/Register pages incorrectly wrapped in `DefaultLayout` (sidebar, app bar)

## What
- Fix missing imports in both form components
- Update router with proper routes and layout handling
- Add nginx SPA fallback config

## Scope
- `frontend/src/views/LoginForm.vue`
- `frontend/src/views/RegistrationForm.vue`
- `frontend/src/router/index.ts`
- `frontend/nginx.conf` (or docker-compose nginx config)