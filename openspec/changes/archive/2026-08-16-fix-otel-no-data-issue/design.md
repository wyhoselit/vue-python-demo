## Context

The observability stack, composed of OpenTelemetry, Prometheus, Grafana, Tempo, and Loki, is failing to display any data. This issue prevents developers from monitoring the application, debugging effectively, and understanding system performance. The `docs/telemetry-verification.md` guide exists but following it reveals the "No Data" problem in Grafana and Prometheus. The root cause is likely a misconfiguration in the data pipeline between the services and the backend monitoring tools.

## Goals / Non-Goals

**Goals:**
- Identify and fix the root cause of the missing telemetry data.
- Ensure metrics, traces, and logs are flowing correctly from the frontend and backend services to the OTel-Collector and then to Prometheus, Tempo, and Loki.
- Document the steps taken and any configuration changes required to resolve the issue.

**Non-Goals:**
- Upgrading versions of any observability components unless strictly necessary for the fix.
- Introducing new monitoring dashboards or alerts.
- Changing the fundamental architecture of the observability stack.

## Decisions

The troubleshooting will follow a systematic, layer-by-layer approach, verifying each step of the telemetry pipeline.

1.  **Verify Service-Level Exporting:**
    *   **Action:** Inspect the logs of the `fastapi-backend` and `frontend` services.
    *   **Rationale:** To confirm that the OTel SDKs are initialized and attempting to export data to the OTel Collector. Look for connection errors or exporter-related warnings.

2.  **Verify OTel Collector Ingestion and Processing:**
    *   **Action:** Add a `logging` exporter to every pipeline in `otel-collector-config.yml` and inspect the Collector's logs.
    *   **Rationale:** The `logging` exporter will print all received data (metrics, traces, logs) to the console. This is the most reliable way to confirm if data is reaching the collector from the services. The current config already has this, which is good.

3.  **Verify OTel Collector to Backend Exporting:**
    *   **Action:** Check the OTel Collector logs for errors related to exporting data to Prometheus, Tempo, or Loki.
    *   **Rationale:** This will isolate issues related to network connectivity between the collector and the backend tools or misconfigurations in the exporter endpoints. For example, ensuring `tempo:4317` and `loki:3100` are resolvable within the Docker network.

4.  **Verify Backend Tool Configuration:**
    *   **Action:**
        *   Prometheus: Check `Status -> Targets` to ensure the `otel-collector` is `UP`.
        *   Grafana: Validate that the datasources for Prometheus, Tempo, and Loki are correctly configured and can connect to their respective services.
    *   **Rationale:** Misconfigurations at this final layer can prevent data from being displayed even if it's being received correctly.

## Risks / Trade-offs

- **[Risk]** Configuration changes might break a previously working part of the pipeline.
    - **Mitigation:** Changes will be made one at a time, and the system will be tested after each change to isolate the impact. Version control will be used for all configuration files.
- **[Risk]** The issue is in the application code itself (e.g., SDK not properly initialized).
    - **Mitigation:** The initial log inspection of the services is designed to catch this early. If suspected, the investigation will shift to the application's telemetry setup code.
