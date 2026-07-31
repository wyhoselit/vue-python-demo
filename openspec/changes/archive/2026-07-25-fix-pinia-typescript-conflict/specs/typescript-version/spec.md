## MODIFIED Requirements

### Requirement: TypeScript version in frontend package.json
The system SHALL use a TypeScript version compatible with Pinia 4.x peer dependencies.

#### Scenario: TypeScript 5.6.0 or higher is installed
- **WHEN** `npm install` is run in the frontend directory
- **THEN** `typescript` package version SHALL be >= 5.6.0
- **AND** `pinia` SHALL install without peer dependency conflicts
- **AND** `npm run build` SHALL complete successfully
- **AND** `npm run test` SHALL complete successfully

#### Scenario: TypeScript version is specified in package.json
- **WHEN** examining `frontend/package.json`
- **THEN** the `devDependencies.typescript` field SHALL specify `^5.6.0` or equivalent range >= 5.6.0

## REMOVED Requirements

### Requirement: TypeScript 5.3.x is used
**Reason**: Incompatible with Pinia 4.x peer dependency requirement (requires TypeScript >= 5.6.0).
**Migration**: Upgrade to TypeScript 5.6.0 or higher as specified in the modified requirement above.