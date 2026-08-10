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

# Helper function to run command with separated stdout/stderr
run_cmd() {
    local cmd="$1"
    local description="$2"
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

run_cmd "cd ${PROJECT_ROOT}/backend; uv run pytest -v" "backend pytest"
run_cmd "cd ${PROJECT_ROOT}/frontend; npm run build" "frontend build"
run_cmd "cd ${PROJECT_ROOT}/frontend; npm test" "frontend test"
run_cmd "cd ${PROJECT_ROOT}; openspec list" "openspec list"
run_cmd "cd ${PROJECT_ROOT}; openspec view" "openspec view"
run_cmd "cd ${PROJECT_ROOT}; podman logs --tail 50 demo_backend_1" "backend logs"
run_cmd "cd ${PROJECT_ROOT}; podman logs --tail 50 demo_frontend_1" "frontend logs"
run_cmd "cd ${PROJECT_ROOT}; podman-compose down && podman-compose up -d --build" "podman-compose up"
run_cmd "cd ${PROJECT_ROOT}; podman-compose ps" "podman-compose ps"
