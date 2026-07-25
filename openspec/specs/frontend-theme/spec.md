# Frontend Theme Management Specification

## Purpose
Defines the theme management system including dark/light mode, Pinia store with localStorage persistence, and Vuetify theme integration.

## Requirements

### Requirement: Theme Pinia Store
The system SHALL provide a Pinia store for theme state management.

#### Scenario: Store exposes dark mode state
- **WHEN** `useThemeStore()` is called
- **THEN** it SHALL return an object with `isDark` state (boolean) and `toggleTheme()` action.

#### Scenario: Dark mode defaults to false
- **WHEN** application initializes without stored preference
- **THEN** `isDark` SHALL default to `false` (light mode).

### Requirement: localStorage persistence
The theme preference SHALL persist across browser sessions.

#### Scenario: Theme saved to localStorage
- **WHEN** `toggleTheme()` is called
- **THEN** the new `isDark` value SHALL be saved to `localStorage.setItem('theme', ...)`.

#### Scenario: Theme loaded from localStorage
- **WHEN** store initializes
- **THEN** it SHALL read `localStorage.getItem('theme')` and set `isDark` accordingly.

### Requirement: Vuetify theme integration
The system SHALL integrate with Vuetify's theme system.

#### Scenario: Vuetify configured with custom themes
- **WHEN** `frontend/src/plugins/vuetify.ts` configures Vuetify
- **THEN** it SHALL define `lightTheme` and `darkTheme` with custom colors:
  - Primary: `#1976D2`
  - Secondary: `#424242`
  - Accent: `#82B1FF`
  - Error: `#FF5252`
  - Info: `#2196F3`
  - Success: `#4CAF50`
  - Warning: `#FB8C00`

#### Scenario: Vuetify uses system theme
- **WHEN** Vuetify is configured
- **THEN** it SHALL use `theme: { defaultTheme: 'light', themes: { lightTheme, darkTheme } }`.

### Requirement: Theme Store initialization
The theme store SHALL be initialized during application bootstrap.

#### Scenario: `initTheme()` called in main.ts
- **WHEN** `frontend/src/main.ts` runs
- **THEN** it SHALL call `themeStore.initTheme()` before mounting the app.

#### Scenario: `initTheme()` reads localStorage
- **WHEN** `initTheme()` is called
- **THEN** it SHALL read the stored theme preference and apply it to the store.