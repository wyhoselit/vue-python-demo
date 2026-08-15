# Grafana Dashboard Verification

## Accessing Grafana
- **URL**: http://localhost:3000
- **Default Credentials**: admin / admin

## Dashboards to Verify
1. **System Overview** - Cluster health, CPU, memory, disk
2. **FastAPI Metrics** - Request rate, latency, error rate
3. **OpenTelemetry Collector** - Traces, metrics, logs throughput
4. **Tempo Traces** - Distributed trace visualization
5. **Loki Logs** - Log aggregation and querying

## Verification Steps
1. Start the full stack:
   ```bash
   docker-compose -f docker-compose.yml -f docker-compose.override.yml up -d
   ```

2. Access Grafana at http://localhost:3000

3. Navigate to Dashboards → Browse

4. Verify each dashboard:
   - **FastAPI Metrics**: Shows requests/sec, p50/p95/p99 latency, error rate
   - **OTel Collector**: Shows received/spans exported counts
   - **Tempo Traces**: Click on traces to see span details
   - **Loki Logs**: Query logs by service label (service="backend", service="frontend")

## Expected Results
- All dashboards load without errors
- Data populates within 1-2 minutes of load test
- No "No data" or error panels
- Queries return results for `service="backend"` and `service="frontend"`

## Troubleshooting
- If no data: Check Prometheus targets are UP
- If traces missing: Check Tempo datasource connection
- If logs missing: Check Loki datasource and log labels