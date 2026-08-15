# Performance Analysis

## Test Setup
- **Tool**: Locust
- **Target**: FastAPI backend (`http://localhost:8000`)
- **Concurrent Users**: 10
- **Duration**: 1 minute
- **Spawn Rate**: 1 user/second

## Test Scenarios
1. **Index Page**: GET `/`
2. **Predict Endpoint**: POST `/predict` with JSON payload

## Expected Results
- Response times should be < 200ms for 95th percentile
- Error rate should be < 1%
- Throughput: ~50-100 requests/second

## Running the Tests
```bash
# Start the application
docker-compose -f docker-compose.yml -f docker-compose.override.yml up -d

# Run Locust load test
locust -f scripts/performance-test.py --headless --users 10 --spawn-rate 1 -t 1m
```

## Analysis Notes
- The application must be running with the observability stack to capture metrics
- Results will be visible in Prometheus/Grafana dashboards
- Traces will appear in Tempo/Jaeger UI