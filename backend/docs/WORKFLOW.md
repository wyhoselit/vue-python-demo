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

## Team Review Guidelines

### Documentation PR Review Checklist

1. **API Contract Changes**
   - [ ] OpenAPI spec changes are intentional
   - [ ] Breaking changes properly documented and approved
   - [ ] Response shapes match consumer expectations

2. **Code Quality**
   - [ ] All public modules have docstrings (module-level `"""`)
   - [ ] All public functions/methods have docstrings
   - [ ] Docstrings follow Google/NumPy style consistently
   - [ ] Type hints present on all public APIs

3. **Documentation Quality**
   - [ ] Changelog entry accurate and descriptive
   - [ ] MkDocs build passes with `--strict`
   - [ ] No broken links or missing assets

4. **Review Process**
   - **Primary reviewer**: API owner or module maintainer
   - **Secondary reviewer**: Cross-team member for cross-cutting concerns
   - **Blocking**: All 162 automated tests must pass
   - **Approval required**: 1 approval minimum

### Review Labels
- `needs-docs-review`: Documentation team attention required
- `api-breaking`: Breaking change requiring extra scrutiny

## Known Issues

### OTEL Collector Unreachable During Docs Build
**Issue**: OTEL Collector endpoint (localhost:4318) occasionally unreachable during docs build, causing trace data fetch to fail.

**Impact**: Non-blocking. Documentation builds complete successfully without trace data. Trace visualization may be temporarily unavailable.

**Status**: MONITORED - No action required until blocking issue identified.

**Mitigation**: Build continues even if Collector is unreachable. No retries or fallbacks currently implemented.
