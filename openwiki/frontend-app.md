---
type: Application
title: Frontend Application
description: Vue 3 + Vuetify frontend single-page application built with Vite and TypeScript.
tags: [vue3, vuetify, vite, typescript, frontend, spa]
---

# Frontend Application

The frontend is a Vue 3 single-page application (SPA) built with Vite and TypeScript, utilizing Vuetify 3 for its Material Design component library.

## Technology Stack

-   **Framework**: Vue 3
-   **Build Tool**: Vite
-   **Language**: TypeScript
-   **UI Framework**: Vuetify 3
-   **Package Manager**: npm

## Key Features

-   **Fast HMR**: Vite provides extremely fast Hot Module Replacement for a smooth development experience.
-   **TypeScript Support**: Enhances code quality and maintainability through static type checking.
-   **Material Design**: Vuetify 3 offers a comprehensive set of pre-built Material Design components.

## Architecture

The frontend is structured as follows:

```
frontend/
├── public/                 # Static assets
├── src/
│   ├── assets/             # Images, icons, etc.
│   ├── components/         # Reusable Vue components
│   ├── plugins/            # Vue plugins (e.g., Vuetify)
│   ├── router/             # Vue Router configuration
│   ├── services/           # API service clients
│   ├── stores/             # Pinia state management
│   ├── __tests__/          # Vitest test suite
│   │   ├── setup.ts        # Test setup and mocks
│   │   ├── components/     # Component tests
│   │   ├── router/         # Router tests
│   │   ├── services/       # API service tests
│   │   └── stores/         # Store tests
│   ├── App.vue             # Main application component
│   └── main.ts             # Application entry point
├── package.json            # Project dependencies and scripts
├── tsconfig.json           # TypeScript configuration
├── vite.config.ts          # Vite build configuration
├── vitest.config.ts        # Vitest configuration
└── Dockerfile              # Docker build instructions
```

### State Management

The application uses Pinia for centralized state management, with stores defined in `src/stores/`.

### Routing

Vue Router is configured in `src/router/` for client-side navigation.

### API Services

API calls are abstracted in `src/services/` using Axios with typed responses.

## Testing

The frontend uses Vitest with Happy DOM for unit testing Vue components and Pinia stores.

```bash
cd frontend
npm run test
```

### Test Structure

- `src/__tests__/setup.ts` - Global test setup with Vuetify CSS mocks
- `src/__tests__/components/App.spec.ts` - Component rendering tests
- `src/__tests__/stores/theme.spec.ts` - Pinia store tests
- `src/__tests__/services/api.spec.ts` - API service tests
- `src/__tests__/router/index.spec.ts` - Router tests

### Test Configuration

`vitest.config.ts` configures:
- Happy DOM environment for browser simulation
- Vuetify component inlining for SSR compatibility
- CSS mocking for Vuetify styles

## Getting Started (Local)

To run the frontend application locally:

1.  **Navigate to the frontend directory:**
    ```bash
    cd frontend
    ```
2.  **Install dependencies:**
    ```bash
    npm install
    ```
3.  **Start the development server:**
    ```bash
    npm run dev
    ```
    The frontend will be accessible at `http://localhost:5173`.

## Source References

-   Main application component: `frontend/src/App.vue`
-   Application entry point: `frontend/src/main.ts`
-   Dependencies: `frontend/package.json`
-   Vite configuration: `frontend/vite.config.ts`
-   Docker build file: `frontend/Dockerfile`
