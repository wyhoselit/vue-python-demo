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
│   ├── App.vue             # Main application component
│   └── main.ts             # Application entry point
├── package.json            # Project dependencies and scripts
├── tsconfig.json           # TypeScript configuration
├── vite.config.ts          # Vite build configuration
└── Dockerfile              # Docker build instructions
```

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
