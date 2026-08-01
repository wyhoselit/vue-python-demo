#!/bin/bash

# https://github.com/Fission-AI/OpenSpec/blob/main/docs/supported-tools.md
# openspec init --tools all
# OpenSpec installs workflow artifacts based on selected workflows:
#     Core profile (default): propose, explore, apply, sync, archive
#     Custom selection: any subset of all workflow IDs: propose, explore, new, continue, apply, ff, sync, archive, bulk-archive, verify, onboard

PROJECT_ROOT="$(dirname "$(realpath "$0")")"
currentdate="$(date +"%Y-%m-%d.%H.%M")"
logfile="${PROJECT_ROOT}/todo/check.$currentdate.log"    

# openspec init --profile custom --tools all
echo "backend pytest  uv run pytest -v " >> $logfile
(cd ${PROJECT_ROOT}/backend; uv run pytest -v 2>&1 | tee -a "$logfile")


echo "frontend npm run build" >> $logfile
(cd ${PROJECT_ROOT}/frontend; npm run build 2>&1 | tee -a "$logfile")
echo "frontend npm test" >> $logfile
(cd ${PROJECT_ROOT}/frontend; npm test 2>&1 | tee -a "$logfile")

# (cd ${PROJECT_ROOT}; podman-compose down && cd ${PROJECT_ROOT}/frontend; npm run dev )

echo "podman-compose down && podman-compose up -d --build" >> $logfile
(cd ${PROJECT_ROOT}; podman-compose down && podman-compose up -d --build 2>&1 | tee -a "$logfile")
echo "podman-compose ps" >> $logfile
(cd ${PROJECT_ROOT}; podman-compose ps 2>&1 | tee -a "$logfile")

echo "openspec list" >> $logfile
(cd ${PROJECT_ROOT}; openspec list 2>&1 | tee -a "$logfile")
# openspec archive add-user-authentication-with-jwt-and-cookiesn
# openspec archive fix-frontend-login-cookie 
# openspec archive fix-login-register-ref-and-404
# openspec archive add-users-me-endpoint
# openspec archive improve-auth-error-handling-and-logging --no-validate
# openspec archive fix-auto-migration-on-startup
# openspec list

echo "openspec view" >> $logfile
(cd ${PROJECT_ROOT}; openspec view 2>&1 | tee -a "$logfile")

(cd ${PROJECT_ROOT}; podman logs --tail 50 demo_backend_1 2>&1 | tee -a "$logfile")
(cd ${PROJECT_ROOT}; podman logs --tail 50 demo_frontend_1 2>&1 | tee -a "$logfile")
