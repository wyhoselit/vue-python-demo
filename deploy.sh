#!/bin/bash

# https://github.com/Fission-AI/OpenSpec/blob/main/docs/supported-tools.md
# openspec init --tools all
# OpenSpec installs workflow artifacts based on selected workflows:
#     Core profile (default): propose, explore, apply, sync, archive
#     Custom selection: any subset of all workflow IDs: propose, explore, new, continue, apply, ff, sync, archive, bulk-archive, verify, onboard

PROJECT_ROOT="$(dirname "$(realpath "$0")")"
currentdate="$(date +"%m-%d.%H.%M")"
normal_logfile="${PROJECT_ROOT}/todo/normal.$currentdate.log"
error_logfile="${PROJECT_ROOT}/todo/error.$currentdate.log"

# Create log files
touch "$normal_logfile" "$error_logfile"

echo "--------------------------------------------------"
echo "logs files: $normal_logfile, $error_logfile"
echo "--------------------------------------------------"

# Helper function to run command with separated stdout/stderr
run_cmd() {
    local cmd="$1"
    local description="$2"
    echo "$cmd" | tee -a "$normal_logfile" "$error_logfile"

    echo "[$description]" | tee -a "$normal_logfile" "$error_logfile"
    eval "$cmd" >>"$normal_logfile" 2>>"$error_logfile"
    local exit_code=$?
    if [ $exit_code -ne 0 ]; then
        echo "[$description] FAILED (exit code: $exit_code)" | tee -a "$normal_logfile" "$error_logfile"
    else
        echo "[$description] OK" | tee -a "$normal_logfile"
    fi
    return $exit_code
}
# Detect compose command
COMPOSE_CMD=""
if command -v podman-compose &> /dev/null; then
    COMPOSE_CMD="podman-compose"
elif command -v docker-compose &> /dev/null; then
    COMPOSE_CMD="docker-compose"
else
    echo "Error: Neither podman-compose nor docker-compose found." | tee -a "$normal_logfile" "$error_logfile"
    exit 1
fi
echo "Using compose command: $COMPOSE_CMD" | tee -a "$normal_logfile" "$error_logfile"

run_cmd "cd ${PROJECT_ROOT}/backend; OTEL_COLLECTOR_ENDPOINT=localhost:4317 uv run python -m pytest -v" "backend pytest"
run_cmd "cd ${PROJECT_ROOT}/frontend; npm test" "frontend test"
run_cmd "cd ${PROJECT_ROOT}/frontend; npm run build" "frontend build"
run_cmd "cd ${PROJECT_ROOT}; openspec list" "openspec list"
run_cmd "cd ${PROJECT_ROOT}; openspec view" "openspec view"



run_cmd "cd ${PROJECT_ROOT}; $COMPOSE_CMD -f docker-compose.yml -f docker-compose.override.yml down && $COMPOSE_CMD -f docker-compose.yml -f docker-compose.override.yml --verbose build" "$COMPOSE_CMD build"
run_cmd "cd ${PROJECT_ROOT}; $COMPOSE_CMD -f docker-compose.yml -f docker-compose.override.yml --verbose up -d --build --force-recreate" "$COMPOSE_CMD up -d recreate build"
# Use generic 'podman' or 'docker' logs based on COMPOSE_CMD
if [ "$COMPOSE_CMD" = "podman-compose" ]; then
    LOGS_CMD="podman logs"
else
    LOGS_CMD="docker logs"
fi
run_cmd "cd ${PROJECT_ROOT}; $LOGS_CMD logs --tail 50 backend" "backend logs"
run_cmd "cd ${PROJECT_ROOT}; $LOGS_CMD logs --tail 50 frontend" "frontend logs"
run_cmd "cd ${PROJECT_ROOT}; $LOGS_CMD logs --tail 50 otel-collector" "otel-collector logs"
run_cmd "cd ${PROJECT_ROOT}; $LOGS_CMD logs --tail 50 prometheus" "prometheus logs"
run_cmd "cd ${PROJECT_ROOT}; $LOGS_CMD logs --tail 50 grafana" "grafana logs"
run_cmd "cd ${PROJECT_ROOT}; $LOGS_CMD logs --tail 50 loki" "loki logs"
run_cmd "cd ${PROJECT_ROOT}; $LOGS_CMD logs --tail 50 tempo" "tempo logs"


run_cmd "cd ${PROJECT_ROOT}; $COMPOSE_CMD ps" "$COMPOSE_CMD ps"
