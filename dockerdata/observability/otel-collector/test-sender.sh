#!/bin/sh
#get url from args default http://otel-collector:4318
URL=${1:-http://otel-collector:4318}
echo "Sending test data to $URL"

curl -X POST $URL/v1/traces \
  -H "Content-Type: application/json" \
  -d '{
    "resourceSpans": [{
      "resource": {
        "attributes": [{"key": "service.name", "value": {"stringValue": "test-service"}}]
      },
      "instrumentationSpans": [{
        "name": "test-span",
        "kind": "SPAN_KIND_CLIENT",
        "status": {"code": "STATUS_CODE_OK"}
      }]
    }]
  }'

echo "Test data sent to OTLP collector"