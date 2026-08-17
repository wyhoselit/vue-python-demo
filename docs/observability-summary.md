# Observability Frontend and Grafana Summary

This document summarizes the troubleshooting and resolution of frontend observability issues and Grafana dashboard provisioning problems.

## Frontend Observability Fixes

### Summary of Completed Work
- **Grafana Dashboard Update**: The dashboard `frontend-observability.json` was updated to use `http_server_duration_milliseconds` metrics, with the version incremented. Key panels for HTTP request duration, API request rate, and page load performance are now functional.
- **OpenTelemetry Collector CORS Issue**:
    - **Problem**: The frontend OTLP Exporter was using the wrong port (4317 for gRPC instead of 4318 for HTTP) and the OTel Collector's CORS configuration was missing the frontend's origin.
    - **Resolution**:
        1. Corrected the OTLP Collector URL in `frontend/src/observability.ts` to `http://localhost:4318`.
        2. Added `http://localhost:4317` to `allowed_origins` in `collector-config.yml`.
- **Missing Frontend Data and Test Failures**:
    - **Problem**: No frontend data appeared in Loki/Tempo, and unit tests failed because a shared `tracer` object was `undefined`.
    - **Resolution**:
        1. Consolidated observability configuration into a single file: `frontend/src/modules/core/observability.ts`.
        2. Exported the `tracer` variable correctly from this file.
        3. All 58 frontend unit tests now pass, and the full container deployment script runs successfully.

---

## Grafana Provisioning Debugging

### Problem Description
Grafana dashboards were not being automatically loaded via the provisioning mechanism.

### Debugging and Resolution
- **Initial Check**: The `grafana` service was defined in `docker-compose.override.yml` with volume mounts for dashboard and datasource provisioning files.
- **Hypothesis 1 (Permissions)**: Suspected a file permission issue, similar to one found with the `loki` service. Adding `user: "0"` to the Grafana service definition did not resolve the issue.
- **Hypothesis 2 (Missing Config)**: By executing into the container, it was discovered that `dashboards.yml` (the provisioning *configuration* file) was not mounted, only the directory containing the dashboards themselves.
- **Resolution**:
    - The `docker-compose.override.yml` was updated to include a volume mount for `dashboards.yml`:
      ```yaml
      - ./dockerdata/observability/grafana/provisioning/dashboards.yml:/etc/grafana/provisioning/dashboards.yml
      ```
    - This change, combined with the earlier permission fix, resolved the provisioning failure. Dashboards are now loaded automatically on startup.
