#!/bin/bash


(cd /code/vue-python-demo/backend; uv run pytest -v)


(cd /code/vue-python-demo/frontend; npm run build )
(cd /code/vue-python-demo/frontend; npm test )

# (cd /code/vue-python-demo/; podman-compose down && cd /code/vue-python-demo/frontend; npm run dev )


(cd /code/vue-python-demo/; podman-compose down && podman-compose up -d --build)
(cd /code/vue-python-demo/; podman-compose ps )

openspec list
# openspec archive add-user-authentication-with-jwt-and-cookiesn
# openspec archive fix-frontend-login-cookie 
# openspec archive fix-login-register-ref-and-404
# openspec archive add-users-me-endpoint
# openspec archive improve-auth-error-handling-and-logging --no-validate
# openspec archive fix-auto-migration-on-startup
# openspec list

openspec status
# (cd /code/vue-python-demo/; gitnexus analyze .)
# (cd /code/vue-python-demo/; gitnexus wiki .)
# (cd /code/vue-python-demo/; openwiki --update )

# (cd /code/vue-python-demo/; openwiki "Please generate documentation for this repository"  )