# Frontend State Management Specification

## Purpose
Defines Pinia stores for global state management including theme and authentication.

## Requirements

### Requirement: Theme Store
The system SHALL provide a Pinia store for theme management (defined in `frontend/src/stores/theme.ts`).

#### Scenario: Theme store exposes required API
- **WHEN** `useThemeStore()` is called
- **THEN** it SHALL provide:
  - `isDark` (computed/ref): current theme state
  - `toggleTheme()` (action): toggles theme and persists to localStorage
  - `initTheme()` (action): initializes theme from localStorage

### Requirement: Authentication Store
The system SHALL provide a Pinia store for authentication state (defined in `frontend/src/stores/auth.ts`).

#### Scenario: Auth store exposes required API
- **WHEN** `useAuthStore()` is called
- **THEN** it SHALL provide:
  - `user` (state): current user object or null
  - `setUser(user)` (action): sets user state
  - `logout()` (action): clears user state
  - `isAuthenticated` (computed): boolean indicating auth status

### Requirement: Store registration
Both stores SHALL be registered with Pinia during application initialization.

#### Scenario: Stores available in components
- **WHEN** a component calls `useThemeStore()` or `useAuthStore()`
- **THEN** the store instance SHALL be available and reactive.

### Requirement: Store persistence
Stores SHALL persist relevant state to localStorage where appropriate.

#### Scenario: Theme persists
- **WHEN** `toggleTheme()` is called
- **THEN** preference SHALL be saved to localStorage.

#### Scenario: Auth state persists (optional)
- **WHEN** user logs in
- **THEN** auth token/user MAY be persisted to localStorage/cookies.