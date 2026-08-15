#!/bin/bash

# ANSI color codes
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Helper function to show service logs on failure
show_service_logs() {
    local service=$1
    local lines=${2:-50}



    echo -e "   ${YELLOW}Showing recent logs for $service:${NC}"
    podman-compose logs --tail=$lines $service 2>/dev/null | grep -E -i "error|fail|exception|panic|fatal|critical|warning" | head -20 || echo "   No obvious errors in recent logs."
    echo ""
}

echo "🔍 Running Observability Stack Health Checks..."

# 1. Docker Containers Check
echo "1. Checking Docker container status..."
if ! podman-compose ps | grep -v "Up" | grep -q "vue-python-demo"; then
    echo -e "   ${GREEN}All containers are running.${NC}"
else

    # Show logs for any non-running containers
    for container in $(podman-compose ps   --format "{{.ID}} \t {{.Names}} \t {{.Status}}" | grep -v "Up" | awk '{print $1}'); do
        # echo "container: $container"
        NAME=$(podman inspect $container --format "{{.Name}}")
        # echo "NAME: $NAME"
        #if service contain test- skip
        if [[ $NAME == *"test-"* ]]; then
            echo "Container $NAME is skiped" 
            continue
        fi
        echo -e "   ${RED}Some containers are not running: ${NAME}"

        show_service_logs $container
    done
fi

# 2. Prometheus Health Check
echo -n "2. Prometheus 'up' status: "
if curl -s "http://localhost:9090/api/v1/query?query=up" | grep -q '"instance":"otel-collector:8889"'; then
    echo -e "${GREEN}OK${NC}"
else
    echo -e "${RED}FAIL${NC}"
    echo "   Reason: Could not find 'otel-collector:8889' target in Prometheus."
    show_service_logs prometheus
fi

# 3. Prometheus Metrics Check
echo -n "3. Prometheus metrics received: "
if curl -s "http://localhost:9090/api/v1/query?query=http_server_duration_milliseconds_count_total" | grep -q '"result":\[{"metric"'; then
    echo -e "${GREEN}OK${NC}"
else
    echo -e "${RED}FAIL${NC}"
    echo "   Reason: No metrics found for 'http_server_duration_milliseconds_count'."
    show_service_logs prometheus
fi

# 4. Loki Health Check
echo -n "4. Loki readiness: "
if curl -s "http://localhost:3100/ready" | grep -q "ready"; then
    echo -e "${GREEN}OK${NC}"
else
    echo -e "${RED}FAIL${NC}"
    echo "   Reason: Loki is not ready."
    show_service_logs loki
fi

# 5. Loki Logs Check
echo -n "5. Loki logs received: "
if curl -s -G "http://localhost:3100/loki/api/v1/query" --data-urlencode 'query={job="fastapi-backend"}' | grep -q '"streams"'; then
    echo -e "${GREEN}OK${NC}"
else
    echo -e "${RED}FAIL${NC}"
    echo "   Reason: No logs found for job 'fastapi-backend'."
    show_service_logs loki
fi

# 6. Tempo Health Check
echo -n "6. Tempo readiness: "
if curl -s "http://localhost:3200/ready" | grep -q "ready"; then
    echo -e "${GREEN}OK${NC}"
else
    echo -e "${RED}FAIL${NC}"
    echo "   Reason: Tempo is not ready."
    show_service_logs tempo
fi

# 7. Grafana Health Check
echo -n "7. Grafana readiness: "
for i in {1..10}; do
    if curl -s "http://localhost:3000/api/health" | jq -e '.database == "ok"' >/dev/null; then
        echo -e "${GREEN}OK${NC}"
        break
    fi
    sleep 3
done
if [ $i -eq 10 ]; then
    echo -e "${RED}FAIL${NC}"
    echo "   Reason: Grafana is not ready."
    show_service_logs grafana
fi


echo "✅ Health checks complete."
