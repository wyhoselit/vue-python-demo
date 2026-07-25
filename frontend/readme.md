# Frontend

Vue 3 + Vuetify 3 AI Platform Frontend

## Prerequisites

- Node.js 18+ 
- npm 9+

## Installation

```bash
cd frontend
npm install
```

## Development

```bash
npm run dev
```

## Building

```bash
npm run build
```

## Testing

### Run all tests
```bash
npm test
```

### Run tests in watch mode
```bash
npm run test:watch
```

### Run tests with coverage
```bash
npm run test:coverage
```

### Open Vitest UI
```bash
npm run test:ui
```

## Project Structure

```
src/
├── layouts/          # Layout components
│   └── DefaultLayout.vue
├── stores/           # Pinia stores
│   ├── theme.ts
│   └── auth.ts
├── views/            # Page components
│   └── Dashboard.vue
├── composables/      # Vue composables
│   └── useApi.ts
├── components/       # Reusable components
├── plugins/          # Vue plugins
│   └── vuetify.ts
├── router/           # Vue Router
│   └── index.ts
└── __tests__/        # Vitest tests
    ├── layouts/
    ├── stores/
    ├── views/
    └── composables/
```

## Theme

The application supports light and dark themes. Toggle via the theme button in the AppBar.

## API Service

The `useApi` composable provides a typed interface to the Backend API:

```typescript
const api = useApi()
const data = await api.get('/endpoint')
```