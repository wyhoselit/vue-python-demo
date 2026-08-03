## Context

Currently, the admin page displays all sections (System Info, Tracing Config, Logs) on a single page at `/admin`. The implementation is in `AdminStatus.vue` which fetches all data and renders everything together.

## Goals / Non-Goals

**Goals:**
- Create separate navigation for admin sections
- Provide cleaner user experience with dedicated pages
- Modularize code for better maintainability

**Non-Goals:**
- Changing API endpoints
- Modifying backend logic

## Decisions

**Router Structure:**
- `/admin` → redirects to `/admin/info`
- `/admin/info` → System information page
- `/admin/logs` → Logs viewer page
- `/admin/settings` → Settings management page

**Component Organization:**
- Create new Vue components for each section
- Extract shared API calls to `admin-endpoints.ts`
- Add navigation sidebar using Vue Router's view pattern

**Navigation:**
- Add sidebar navigation component
- Use `<router-link>` for navigation between sections
- Apply active styling to current page

## Risks / Trade-offs

[Risk] Multiple API calls on navigation → Mitigation: Use Vue's reactive composition to handle loading states
[Risk] Breaking existing bookmarks to /admin → Mitigation: Add redirect from /admin to /admin/info

## Open Questions

- Should navigation persist across all admin pages?
- What layout pattern for sidebar (fixed vs collapsible)?