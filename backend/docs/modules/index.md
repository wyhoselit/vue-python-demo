# Internal Modules Documentation

## Architecture

The backend follows a modular monolith architecture. Each module is self-contained under `app/modules/`.

### Core Layers

- **API** — Controller layer handling HTTP requests and responses
- **Services** — Business logic and orchestration
- **Models** — Database models and schemas
- **Middleware** — Cross-cutting concerns like logging and security

## Module List

### [Core](core/config.md)
Shared utilities, configuration, database connectivity, and base exceptions.

### [AI](ai/llm_service.md)
LLM integration, RAG pipeline, and vector store management.

### [User](user/user.md)
User management, authentication, and role-based access control.

### Admin
Administrative status reporting and log viewing.

### System
System-wide health checks and configuration management.

## Contributing

When adding new modules:

1. Follow the directory structure: `app/modules/<name>/`
2. Add Google-style docstrings to all public functions and classes
3. Add a corresponding page under `docs/modules/`
4. Update `mkdocs.yml` navigation