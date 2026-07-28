#!/bin/bash

# https://github.com/Fission-AI/OpenSpec/blob/main/docs/supported-tools.md
# openspec init --tools all
# OpenSpec installs workflow artifacts based on selected workflows:
#     Core profile (default): propose, explore, apply, sync, archive
#     Custom selection: any subset of all workflow IDs: propose, explore, new, continue, apply, ff, sync, archive, bulk-archive, verify, onboard

# openspec init --profile custom --tools all


(cd /code/vue-python-demo/backend; uv run pytest -v)


(cd /code/vue-python-demo/frontend; npm run build )
(cd /code/vue-python-demo/frontend; npm test )

# (cd /code/vue-python-demo/; podman-compose down && cd /code/vue-python-demo/frontend; npm run dev )


(cd /code/vue-python-demo/; podman-compose down && podman-compose up -d --build)
(cd /code/vue-python-demo/; podman-compose ps )

(cd /code/vue-python-demo/; openspec list)
# openspec archive add-user-authentication-with-jwt-and-cookiesn
# openspec archive fix-frontend-login-cookie 
# openspec archive fix-login-register-ref-and-404
# openspec archive add-users-me-endpoint
# openspec archive improve-auth-error-handling-and-logging --no-validate
# openspec archive fix-auto-migration-on-startup
# openspec list

(cd /code/vue-python-demo/; openspec view)

