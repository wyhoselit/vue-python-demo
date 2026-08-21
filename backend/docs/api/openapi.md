# OpenAPI Specification

This page displays the current OpenAPI specification for the backend API.

The specification is automatically generated from the FastAPI application and updated on every merge to main.

## Interactive Spec

<div id="redoc-container"></div>

<script src="https://cdn.jsdelivr.net/npm/redoc@next/bundles/redoc.standalone.js"></script>
<script>
  Redoc.init(
    "../openapi/openapi.json",
    {
      scrollYOffset: 60,
      hideHostname: true,
      expandResponses: "200,201",
      pathInMiddlePanel: true
    },
    document.getElementById("redoc-container")
  );
</script>

!!! note
    This spec is generated from source code. Do not edit manually.
    Use `scripts/update_openapi.py` to regenerate.