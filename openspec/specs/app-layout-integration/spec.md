## ADDED Requirements

### Requirement: App.vue uses DefaultLayout with RouterView
The system SHALL render DefaultLayout as the root component in App.vue, which contains AppBar, NavigationDrawer, and RouterView for page content.

#### Scenario: App.vue renders DefaultLayout
- **WHEN** application loads
- **THEN** App.vue renders DefaultLayout with RouterView inside

#### Scenario: Dashboard page displays within layout
- **WHEN** user navigates to root path "/"
- **THEN** Dashboard.vue renders inside DefaultLayout's RouterView
- **AND** AppBar shows "AI Platform" title
- **AND** NavigationDrawer shows Dashboard menu item
- **AND** dark mode toggle appears in AppBar

### Requirement: Build configuration excludes test files from type checking
The system SHALL configure vue-tsc to exclude `__tests__` directory to prevent test mock type errors during build.

#### Scenario: Build succeeds without test type errors
- **WHEN** running `npm run build`
- **THEN** vite build completes successfully
- **AND** vue-tsc does not report errors from test files

### Requirement: Frontend proposal validation for Layout integration
The system SHALL enforce validation rules in frontend proposals that check App.vue correctly uses Layout component structure.

#### Scenario: Frontend proposal validation
- **WHEN** creating a new frontend proposal
- **THEN** a validation rule checks that App.vue imports and uses DefaultLayout with RouterView