## Context
- LoginForm.vue line 67: `const form = ref<HTMLFormElement | null>(null)` but `ref` not imported
- RegistrationForm.vue same issue
- Router only has `/` (Dashboard), missing `/login` and `/register`
- DefaultLayout adds sidebar/app-bar inappropriate for auth pages

## Goals / Non-Goals
**Goals:**
- Fix `ref` import in both forms
- Add `/login` and `/register` routes
- Create `AuthLayout.vue` (minimal, no sidebar)
- Configure nginx `try_files $uri $uri/ /index.html`

**Non-Goals:**
- Add password validation rules
- Implement remember-me

## Decisions
1. **Layout Strategy**: New `AuthLayout.vue` with just `<router-view />` + centered card container
2. **Router**: Lazy-load auth views, `meta: { requiresAuth: false, layout: 'auth' }`
3. **Nginx**: Add `try_files` in `location /` block

## Risks / Trade-offs
- New layout file adds minimal complexity
- Need to rebuild frontend Docker image for nginx config