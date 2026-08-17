#!/bin/bash



echo "=== Prometheus Metrics ===" && curl -s "http://localhost:9090/api/v1/label/__name__/values" | jq '.data[]' | head -40 && echo "=== Prometheus Targets ===" && curl -s "http://localhost:9090/api/v1/targets" | jq '.data.activeTargets[] | {scrapePool, health, lastError, labels}' && echo "=== Loki Labels ===" && curl -G -s "http://localhost:3100/loki/api/v1/labels" | jq && echo "=== Loki Label Values (job) ===" && curl -G -s "http://localhost:3100/loki/api/v1/label/job/values" | jq && echo "=== Loki Label Values (exporter) ===" && curl -G -s "http://localhost:3100/loki/api/v1/label/exporter/values" | jq && echo "=== Loki Label Values (level) ===" && curl -G -s "http://localhost:3100/loki/api/v1/label/level/values" | jq > metrics-and-labels.txt

echo "=== Loki query (all logs, last 1h) ===" && curl -G -s "http://localhost:3100/loki/api/v1/query_range" --data-urlencode 'query={job=~".+"}' --data-urlencode 'limit=5' --data-urlencode "start=$(date -u -d '1 hour ago' +%s)000000000" --data-urlencode "end=$(date -u +%s)000000000" | jq '.data.result[] | {stream: .stream, values_count: (.values | length), first_value: .values[0]}' && echo "=== Prometheus sample metric query ===" && curl -s "http://localhost:9090/api/v1/query?query=up" | jq '.data.result' >> metrics-and-labels.txt

 echo "=== All Prometheus metric names from otel-collector ===" && curl -s "http://localhost:8889/metrics" | grep -v "^#" | grep -v "^$" | awk -F'{' '{print $1}' | sort -u | head -60   >> metrics-and-labels.txt


 curl -s "http://localhost:8889/metrics" | head -30 >> metrics-and-labels.txt


 echo "=== Try backend /metrics ===" && curl -s "http://localhost:8000/metrics" | head -40 && echo "=== Collector config ===" && cat dockerdata/observability/otel-collector/collector-config.yml >> metrics-and-labels.txt

 