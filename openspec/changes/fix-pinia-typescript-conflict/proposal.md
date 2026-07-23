## Why

Attempting to install `pinia` for the frontend tests encountered a peer dependency conflict: Pinia 4.x requires `typescript >= 5.6.0`, but the project uses `typescript ~5.3.3`. This blocks the `add-tests-for-all-features` change from completing. The TypeScript version must be upgraded to resolve this.

## What Changes

- Update `frontend/package.json`: Change `typescript` version from `~5.3.3` to `^5.6.0` or higher.
- Update related devDependencies if needed (`vue-tsc`, `@vue/language-core`) to versions compatible with the new TypeScript.
- Run `npm install` to update lock file.
- Verify no breaking changes in TypeScript or related tools.

## Capabilities

### New Capabilities
- (None - this is a dependency version fix)

### Modified Capabilities
- `typescript-version`: The project's TypeScript version requirement is increased to satisfy Pinia's peer dependency.

## Impact

- Modified: `frontend/package.json` (typescript version)
- New: `package-lock.json` (updated by npm install)
- No changes to application source code.
- May require developers to update their Node.js environment if they have strict version constraints.
- Potential for minor breaking changes in TypeScript compilation; must verify build succeeds.
