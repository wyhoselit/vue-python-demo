# Frontend Testing Specification

## Purpose
Defines the testing strategy and infrastructure for the frontend application using Vitest and Vue Test Utils.

## Requirements

### Requirement: Vitest setup
The system SHALL configure Vitest for unit and component testing.

#### Scenario: Vitest configuration exists
- **WHEN** `frontend/vitest.config.ts` is present
- **THEN** it SHALL configure:
  - `@vue/test-utils` for Vue component testing
  - `happy-dom` as the test environment
  - Path aliases (`@/*`)

### Requirement: Test scripts
The system SHALL provide NPM scripts for running tests.

#### Scenario: `npm test` runs Vitest
- **WHEN** `npm test` is executed in `frontend/`
- **THEN** Vitest SHALL run all `.spec.ts` or `.test.ts` files.

### Requirement: Component testing
The system SHALL include tests for key UI components.

#### Scenario: `DefaultLayout` is tested
- **WHEN** `frontend/src/__tests__/layouts/DefaultLayout.test.ts` exists
- **THEN** it SHALL verify rendering, responsiveness, and dark mode toggle.

### Requirement: Store testing
The system SHALL include tests for Pinia stores.

#### Scenario: `theme` store is tested
- **WHEN** `frontend/src/__tests__/stores/theme.test.ts` exists
- **THEN** it SHALL verify state, actions (toggleTheme, initTheme), and localStorage persistence.

#### Scenario: `auth` store is tested
- **WHEN** `frontend/src/__tests__/stores/auth.test.ts` exists
- **THEN** it SHALL verify state structure, `setUser`, and `logout` actions.

### Requirement: Router testing
The system SHALL include tests for Vue Router configuration.

#### Scenario: Router navigation tested
- **WHEN** `frontend/src/__tests__/router/index.spec.ts` exists
- **THEN** it SHALL verify basic navigation and route resolution.

### Requirement: API service testing
The system SHALL include tests for the API service composable.

#### Scenario: `useApi` composable is tested
- **WHEN** `frontend/src/__tests__/composables/useApi.test.ts` exists
- **THEN** it SHALL verify Axios mocking and error handling.

### Requirement: Dashboard view testing
The system SHALL include tests for the Dashboard view.

#### Scenario: Dashboard component tested
- **WHEN** `frontend/src/__tests__/views/Dashboard.test.ts` exists
- **THEN** it SHALL verify rendering and API integration with mocks.

### Requirement: `App.vue` component testing
The system SHALL include tests for the root App component.

#### Scenario: App component tested
- **WHEN** `frontend/src/__tests__/components/App.spec.ts` exists
- **THEN** it SHALL verify correct rendering of `DefaultLayout` and `router-view`.