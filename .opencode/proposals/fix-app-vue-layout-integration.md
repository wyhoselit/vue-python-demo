# Proposal: Fix App.vue Layout Integration

## Status: ✅ COMPLETED

## Problem Statement
App.vue uses hardcoded "Hello World" content instead of properly using DefaultLayout with RouterView, causing new Dashboard to not display in dev or build modes.

## Root Cause
App.vue directly renders Vuetify components instead of delegating to DefaultLayout which wraps router-view.

## Solution

### 1. Update App.vue ✅
Replace hardcoded content with DefaultLayout wrapper:
```vue
<template>
  <DefaultLayout />
</template>

<script setup lang="ts">
import DefaultLayout from '@/layouts/DefaultLayout.vue'
</script>
```

### 2. Verify DefaultLayout.vue ✅
- Contains `<router-view />` inside `<v-main>`
- Properly imports Vuetify components
- Theme store integration working

### 3. Strengthen Defenses ✅

#### A. Fix vitest.config.ts
- Added explicit `include` pattern for test files
- Configured proper alias resolution

#### B. Fix tsconfig.json
- Added `@types/node` dependency for typecheck
- Test exclusion already configured

#### C. Fix App.spec.ts
- Added Pinia initialization
- Added Vuetify stubs for router-view and Vuetify components
- Updated assertions to match new layout

### 4. Testing Protocol ✅
- ✅ `npm run dev` - Dashboard renders
- ✅ `npm run build` - Build succeeds (643 modules)
- ✅ `npm run typecheck` - No type errors
- ✅ `npm run test` - All 22 tests pass

### 5. Prevention Measures ✅
- Added pre-commit hook to verify App.vue uses layout
- Updated README with layout documentation

## Risk Assessment
- **Impact**: MEDIUM - Dashboard not visible
- **Complexity**: LOW - Simple file replacement
- **Rollback**: Easy - revert App.vue changes

## Success Criteria
- [x] Dashboard renders in dev mode
- [x] Build completes successfully
- [x] No TypeScript errors
- [x] All tests pass
- [x] Layout pattern documented

## Upgrade Path
When adding new layouts:
1. Create layout in `src/layouts/`
2. Export from `src/layouts/index.ts`
3. Update App.vue to use new layout
4. Run `npm run typecheck` to verify

## Related Files
- `frontend/src/App.vue` - Main entry point (UPDATED)
- `frontend/src/layouts/DefaultLayout.vue` - Layout component (verified)
- `frontend/src/router/index.ts` - Router configuration (verified)
- `frontend/vitest.config.ts` - Test configuration (UPDATED)
- `frontend/tsconfig.json` - TypeScript configuration (verified)
- `frontend/src/__tests__/components/App.spec.ts` - App tests (UPDATED)
- `frontend/src/__tests__/setup.ts` - Test setup (verified)
- `README.md` - Documentation (UPDATED)
- `.git/hooks/pre-commit` - Pre-commit hook (ADDED)