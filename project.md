# Project Architecture

## Overview
The project follows a business-module architecture. All code is organized by business function (admin, user, dashboard, etc.).

## Directory Structure
- `modules/`: Contains business-specific logic.
- `shared/`: Contains infrastructure shared across 3+ modules.
- `core/` (Backend): Contains application-level infrastructure, security, database settings.
- `tests/`: Business modules follow logic module structure.

## Rules
- Test files must be co-located with their respective modules in `tests/modules/<module-name>/`.
- Avoid cross-module relative imports; use aliases.
- Shared code should only be used if it is strictly shared by 3 or more modules.