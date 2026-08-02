## Why

The current system lacks observability, making it difficult to debug performance bottlenecks and trace individual request flows. Adding a tracing feature will provide visibility into function execution time and help pinpoint issues efficiently.

## What Changes

- Add a tracing decorator for backend functions (FastAPI).
- Add an API endpoint and/or middleware to toggle tracing state.
- Add frontend tracing interceptors (Axios) to record API call durations.
- Implement a configuration storage mechanism (DB) so admin users can toggle tracing state.
- Implement structured logging to store trace events in a database.

## Capabilities

### New Capabilities
- `tracing-backend`: Logic for tracking function performance in FastAPI.
- `tracing-frontend`: Logic for tracking API call duration in the Vue frontend.
- `tracing-config`: Dynamic configuration for toggling tracing on/off.

### Modified Capabilities
- None.

## Impact

- `backend/app/core/`: Will require updates to middleware and logging.
- `backend/app/api/`: Will require a new endpoint for admin tracing configuration.
- `frontend/src/services/api.ts`: Will require updates to interceptors.
