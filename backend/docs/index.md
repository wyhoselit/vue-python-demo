# Backend API Documentation

## Overview

This documentation provides:

1. **API Reference** — Auto-generated OpenAPI spec for all FastAPI endpoints
2. **Internal Module Documentation** — Detailed reference for Python modules, classes, and functions

## Documentation System

- **mkdocs-material** — Theme and build system
- **mkdocstrings** — Python documentation extraction with Google-style docstrings
- **Redoc** — Interactive OpenAPI viewer embedded in mkdocs
- **oasdiff** — OpenAPI diff checking for breaking changes

## How to Build Locally

```bash
# Install dependencies
uv pip install mkdocs-material "mkdocstrings[python]"

# Build documentation
mkdocs build --strict

# Serve locally
mkdocs serve
```

## CI/CD Integration

Documentation is built and validated in `.github/workflows/docs.yml`:

- OpenAPI spec is fetched from a fresh server start
- mkdocs builds with `--strict` mode
- oasdiff compares against the baseline on main branch