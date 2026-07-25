# Frontend Layout System Specification

## Purpose
Defines the main layout structure of the frontend application including the AppBar, NavigationDrawer, and RouterView integration.

## Requirements

### Requirement: Default Layout component
The system SHALL provide a `DefaultLayout` component that serves as the main layout wrapper.

#### Scenario: Layout contains AppBar
- **WHEN** `DefaultLayout` is rendered
- **THEN** it SHALL include a `v-app-bar` with:
  - Navigation drawer toggle button
  - Application title "AI Platform"
  - Theme toggle button

#### Scenario: Layout contains NavigationDrawer
- **WHEN** `DefaultLayout` is rendered
- **THEN** it SHALL include a `v-navigation-drawer` with:
  - Temporary drawer for mobile (smAndDown)
  - Permanent side drawer for desktop
  - Navigation items linking to Dashboard

#### Scenario: Layout contains RouterView
- **WHEN** `DefaultLayout` is rendered
- **THEN** it SHALL include a `<router-view />` component inside `v-main` for page content rendering.

### Requirement: Responsive design
The layout SHALL adapt to different screen sizes.

#### Scenario: Mobile drawer behavior
- **WHEN** viewport is mobile (smAndDown)
- **THEN** the navigation drawer SHALL be temporary and close on navigation.

#### Scenario: Desktop drawer behavior
- **WHEN** viewport is desktop (not smAndDown)
- **THEN** the side navigation drawer SHALL be permanent and always visible.

### Requirement: Theme integration
The layout SHALL integrate with the theme management system.

#### Scenario: Dark mode toggle
- **WHEN** user clicks theme toggle in AppBar
- **THEN** it SHALL call `themeStore.toggleTheme()` to switch between light/dark modes.

#### Scenario: Theme icon reflects current mode
- **WHEN** theme is dark
- **THEN** AppBar SHALL show 'mdi:weather-sunny' icon.
- **WHEN** theme is light
- **THEN** AppBar SHALL show 'mdi:weather-night' icon.

### Requirement: Navigation items
The layout SHALL provide navigation to application pages.

#### Scenario: Dashboard navigation
- **WHEN** user clicks "Dashboard" in NavigationDrawer
- **THEN** application SHALL navigate to root path "/".