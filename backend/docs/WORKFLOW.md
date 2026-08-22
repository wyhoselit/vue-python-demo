# Documentation Workflow

The project uses an automated documentation system with OpenAPI, MkDocs Material, and CI validation.

## Automated Updates
A script is provided to automate the documentation update process:
`./scripts/docs-update.sh "description of changes"`

This script:
1. Updates the `master` branch
2. Creates a new documentation branch
3. Regenerates the OpenAPI specification
4. Builds the documentation with `--strict` validation
5. Creates a dated changelog entry in `docs/changelog/`
6. Commits changes, pushes the branch, and creates a GitHub PR

## Continuous Integration
Documentation is validated automatically on every PR to `master`:
- **OpenAPI Breaking Change Detection**: Using `oasdiff` against the `master` baseline
- **Documentation Build**: Using `mkdocs build --strict`
- **Changelog Generation**: Summary of API changes added to the GitHub PR

## Manual Verification
To build and verify documentation locally:
```bash
cd backend
PYTHONPATH=. uv run python scripts/update_openapi.py
uv run mkdocs build --strict
uv run mkdocs serve
```
