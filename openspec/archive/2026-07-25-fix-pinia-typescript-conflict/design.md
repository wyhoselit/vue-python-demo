## Context

The frontend project requires Pinia for state management testing in the `add-tests-for-all-features` change. Installing Pinia 4.x fails because it requires `typescript >= 5.6.0`, but `frontend/package.json` specifies `typescript: "~5.3.3"`. This TypeScript version is incompatible with Pinia's peer dependency requirements.

## Goals / Non-Goals

**Goals:**
- Upgrade TypeScript to version 5.6.0 or higher in `frontend/package.json`.
- Ensure all related devDependencies (`vue-tsc`, `@vue/language-core`) remain compatible.
- Verify the project still builds and tests pass after the upgrade.

**Non-Goals:**
- Migrate to TypeScript 6.x or newer.
- Refactor any TypeScript code that might be affected by the upgrade (minor version changes should be safe).
- Update other package versions unrelated to the TypeScript upgrade.

## Decisions

### 1. TypeScript Version Upgrade
**Choice:** Upgrade to `^5.6.0` (the minimum required by Pinia).
**Rationale:** This is the smallest version bump that resolves the peer dependency conflict. It minimizes the risk of introducing breaking changes compared to jumping to a newer major version.
**Alternatives Considered:**
- `~5.3.3` with legacy peer deps (`npm install --legacy-peer-deps`): Not recommended as it may hide underlying incompatibilities.
- TypeScript 6.x: Higher risk of breaking changes; unnecessary for this fix.

### 2. Related Package Updates
**Choice:** Let npm resolve compatible versions for `vue-tsc` and `@vue/language-core` automatically via `npm install`.
**Rationale:** These packages are tightly coupled with TypeScript and Vue. Using npm's resolution ensures compatibility.

## Risks / Trade-offs

| Risk | Mitigation |
|------|------------|
| TypeScript 5.6.0 introduces breaking changes | Run `npm run build` and `npm run test` to verify. Minor version changes are usually safe. |
| Vue or Vuetify might not be compatible | Check Vuetify and Vue documentation for TypeScript 5.6 compatibility. |
| Lock file mismatch in team environments | Commit updated `package-lock.json` and communicate the change. |

## Migration Plan

1. Update `frontend/package.json` TypeScript version.
2. Run `npm install` to update dependencies and lock file.
3. Run `npm run build` to verify compilation succeeds.
4. Run `npm run test` to verify tests pass.
5. Commit `package.json` and `package-lock.json`.

## Open Questions

- Are there any explicit TypeScript 5.x features in the codebase that might be affected by the minor version upgrade? (Likely no, but should verify).