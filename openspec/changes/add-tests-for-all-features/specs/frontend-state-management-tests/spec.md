## ADDED Requirements

### Requirement: Pinia store state can be initialized and read
The system SHALL have tests to verify Pinia store state management.

#### Scenario: Theme store initializes with default theme
- **WHEN** `useThemeStore` is created
- **THEN** its `theme` state SHALL be set to a default value (e.g., 'light').

#### Scenario: Theme store theme can be changed
- **WHEN** `useThemeStore.setTheme('dark')` is called
- **THEN** the `theme` state SHALL update to 'dark'.

### Requirement: Pinia store getters return correct values
The system SHALL have tests for Pinia store getters.

#### Scenario: `isDark` getter returns true for dark theme
- **WHEN** `theme` state is 'dark'
- **THEN** `useThemeStore.isDark` getter SHALL return `true`.

### Requirement: Pinia store actions modify state correctly
The system SHALL have tests for Pinia store actions.

#### Scenario: Toggle theme action switches theme
- **WHEN** `useThemeStore.toggleTheme()` is called
- **THEN** the `theme` state SHALL switch from 'light' to 'dark' or vice versa.
