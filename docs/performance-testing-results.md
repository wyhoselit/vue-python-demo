# Performance Testing Results

## Test Environment
- **Date**: August 14, 2026
- **Application**: vue-python-demo (FastAPI backend + Vue.js frontend)
- **Load Test Tool**: Locust 2.46.3
- **Test Type**: Concurrent user simulation

## Test Scenarios

### Scenario 1: Index Page Load
- **Endpoint**: GET `/`
- **Description**: Load the main index page

### Scenario 2: Prediction Endpoint
- **Endpoint**: POST `/predict`
- **Description**: Submit text for sentiment analysis
- **Payload**: `{"text": "This is a test sentence for sentiment analysis."}`

## Test Configuration
| Parameter | Value |
|-----------|-------|
| Concurrent Users | 10 |
| Spawn Rate | 1 user/second |
| Test Duration | 1 minute |
| Target URL | http://localhost:8000 |

## Expected Metrics
- **Response Time (p50)**: < 100ms
- **Response Time (p95)**: < 200ms
- **Error Rate**: < 1%
- **Throughput**: 50-100 RPS

## Running Tests

### Prerequisites
```bash
# Install Locust
pip install locust

# Start the application
docker-compose -f docker-compose.yml -f docker-compose.override.yml up -d
```

### Execute Load Test
```bash
locust -f scripts/performance-test.py --headless --users 10 --spawn-rate 1 -t 1m
```

## Analyzing Results

### Grafana Dashboards
- **URL**: http://localhost:3000
- **Dashboard**: Verify data appears in:
  - FastAPI Metrics (requests, latency)
  - OpenTelemetry Collector (traces per second)
  - Tempo (trace visualization)
  - Prometheus (time-series metrics)

### Prometheus Queries
```
# Average request rate
rate(http_server_requests_seconds_count[1m])

# 95th percentile latency
histogram_quantile(0.95, rate(http_server_requests_seconds_bucket[5m]))

# Error rate
rate(http_server_requests_seconds_count{status=~"5.."}[1m])
```

## Performance Targets
- Response time under 200ms for 95% of requests
- Error rate below 1%
- System remains stable under 10 concurrent users
- No memory leaks or connection pool exhaustion

## Results Summary
*To be filled after test execution*

| Metric | Target | Actual | Status |
|--------|--------|--------|--------|
| p95 Latency | < 200ms | TBD | TBD |
| Error Rate | < 1% | TBD | TBD |
| Throughput | 50-100 RPS | TBD | TBD |