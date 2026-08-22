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

## Automated Workflow

To update documentation when making code changes:

```bash
./scripts/docs-update.sh "description of changes"
```

This script:
1. Updates OpenAPI spec
2. Builds docs locally
3. Creates dated changelog entry
4. Opens PR with CI validation