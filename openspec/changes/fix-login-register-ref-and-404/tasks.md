## 1. Frontend Fixes

- [x] 1.1 Fix `ref` imports in `LoginForm.vue` and `RegistrationForm.vue`
- [x] 1.2 Create `frontend/src/layouts/AuthLayout.vue`
- [x] 1.3 Update `frontend/src/router/index.ts` with `/login` and `/register` routes
- [x] 1.4 Update `App.vue` to dynamically switch layout

## 2. Infrastructure Fixes

- [x] 2.1 Update nginx configuration for SPA fallback (`try_files`)

## 3. Testing

- [x] 3.1 Verify `/login` and `/register` routes load correctly
- [x] 3.2 Verify `ref is not defined` error is gone
- [x] 3.3 Verify auth pages do not render sidebar/navbar