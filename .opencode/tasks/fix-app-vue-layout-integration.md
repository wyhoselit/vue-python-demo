# Tasks: Fix App.vue Layout Integration

## Task List

### Phase 1: Immediate Fix
- [ ] `frontend/src/App.vue` - Replace Hello World with DefaultLayout + RouterView

### Phase 2: Configuration Hardening
- [ ] `frontend/vitest.config.ts` - Add build guard, exclude test files from build
- [ ] `frontend/tsconfig.json` - Verify test exclusion configuration

### Phase 3: Verification
- [ ] Run `npm run dev` - Verify Dashboard renders
- [ ] Run `npm run build` - Verify build succeeds
- [ ] Run `npm run typecheck` - Verify no type errors
- [ ] Run `npm run test` - Verify tests pass

### Phase 4: Prevention
- [ ] Add CI check for App.vue layout usage
- [ ] Document layout pattern in README

## Detailed Actions

### 1. Fix App.vue
**File**: `frontend/src/App.vue`
**Change**: Replace template content with DefaultLayout wrapper

### 2. Harden vitest config
**File**: `frontend/vitest.config.ts`
**Change**: Add explicit exclude patterns for test files in build context

### 3. Verify tsconfig
**File**: `frontend/tsconfig.json`
**Change**: Ensure `"src/__tests__/**"` is in exclude array

## Verification Commands
```bash
cd frontend
npm run dev        # Dev mode check
npm run build      # Build check
npm run typecheck  # Type check
npm run test       # Test suite
```

## Rollback Plan
If issues occur:
1. `git checkout -- frontend/src/App.vue`
2. Revert configuration changes
3. Document issue in AGENTS.md