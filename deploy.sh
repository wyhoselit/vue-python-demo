#!/bin/bash


(cd /code/vue-python-demo/backend; uv run pytest -v)


(cd /code/vue-python-demo/frontend; npm run build )
(cd /code/vue-python-demo/frontend; npm test )

# (cd /code/vue-python-demo/; podman-compose down && cd /code/vue-python-demo/frontend; npm run dev )


(cd /code/vue-python-demo/; podman-compose down && podman-compose up -d --build)
(cd /code/vue-python-demo/; podman-compose ps )



# (cd /code/vue-python-demo/; gitnexus analyze .)
# (cd /code/vue-python-demo/; gitnexus wiki .)
# (cd /code/vue-python-demo/; openwiki --update )

