---
type: Plan
title: Documentation Update Plan
description: Update documentation for recent backend restructuring and API versioning changes.
tags: [plan, backend, restructuring, documentation]
---

# Documentation Update Plan

## Affected Pages
- /openwiki/quickstart.md: Update backend development instructions to reflect module structure (modules/core, modules/admin, etc).
- /openwiki/backend-service.md: New page needed to describe backend modular structure and API versioning.

## Source Evidence
- Git changes: restructured `backend/app` into modules (`admin`, `core`, `dashboard`, `system`, `user`).
- API versioning: `backend/app/api/version_router.py`, `backend/app/api/versioning.py`, `backend/app/api/v2/`.

## Relationships
- Quickstart -> links to -> Backend Service
- Backend Service -> describes -> Modules Structure
- Backend Service -> describes -> API Versioning

## Questions
- Is documentation for individual modules (admin, core) needed or just an overview? Keep overview for now as per "surgical" instruction.
