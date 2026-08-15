# Research Notes

## Overview

This research focuses on designing an OpenTelemetry (OTel) integration with FastAPI and Vue.js. We aim to collect application-level and system metrics, and use Prometheus and Grafana for monitoring.

## Current Decisions

* Use Python (FastAPI) as the backend framework
* Use JavaScript (Vue.js) as the frontend framework
* Use OpenTelemetry Python SDK for Python backend
* Use OpenTelemetry JavaScript SDK for JavaScript frontend
* Use Prometheus Exporter for metrics
* Use OTEL Exporter for traces and logs
* Use OpenTelemetry Collector as the middle layer, receiving data from Python backend and sending it to Prometheus, Jaeger/Tempo, and Loki

## Proposed Architecture

* Docker Compose for deployment
* Use Docker Compose to manage services
* Use Docker Compose to override existing services
* Use `docker-compose.override.yml` to define the configuration
* Use `docker-compose` to run services
* Use `docker-compose` to monitor services

## Future Work

* Implement Zero-code instrumentation
* Implement process code instrumentation
* Implement route management instrumentation
* Implement FastAPI instrumentation
* Implement Pinia/Vuex instrumentation
* Implement FastAPI instrumentation

## Key Takeaways

* Use OpenTelemetry SDKs for Python and JavaScript
* Use Prometheus Exporter for metrics
* Use OTEL Exporter for traces and logs
* Use OpenTelemetry Collector for middle layer
* Use Docker Compose for deployment and management
* Use `docker-compose` to run services and monitor them
* Implement Zero-code instrumentation and process code instrumentation
* Implement route management instrumentation and FastAPI instrumentation

## References

* [OpenTelemetry Python SDK documentation](https://docs.opentelemetry.io/python/docs/)
* [OpenTelemetry JavaScript SDK documentation](https://docs.opentelemetry.io/javascript/docs/)
* [Prometheus documentation](https://prometheus.io/docs/)
* [Grafana documentation](https://grafana.com/docs/)
* [Docker Compose documentation](https://docs.docker.com/compose/)
* [OpenTelemetry Collector documentation](https://docs.opentelemetry.io/collector/docs/)

Please let me know if you have any questions or need further clarification on any of these points.