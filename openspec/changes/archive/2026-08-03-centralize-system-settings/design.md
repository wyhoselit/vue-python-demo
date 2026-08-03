## Context

The system currently manages configurations (like tracing) through scattered, table-specific models and migrations. This increases schema complexity and slows down feature velocity when new settings are required. We need a centralized, schema-flexible approach.

## Goals / Non-Goals

**Goals:**
- Centralize all system-wide settings into a single `system_settings` table.
- Use SQLite native JSON type to allow flexible schema for different config types.
- Simplify configuration management, reducing the need for migrations for each setting.

**Non-Goals:**
- Complete refactor of all existing configurations (only tracing initially, others as needed).
- Moving non-config data (like user profiles) to this table.

## Decisions

- **Storage**: Use SQLite native `JSON` column for storing settings. This provides flexibility without complex schema migrations.
- **Access Pattern**: Provide a central `get_setting(key)` and `set_setting(key, value)` utility.
- **Validation**: Use Pydantic models at the application layer to enforce type safety for stored configurations.

## Risks / Trade-offs

- [Risk] Loss of schema-level constraint validation → [Mitigation] Use Pydantic models to validate the settings object before serialization.
- [Risk] Potential for configuration key collisions → [Mitigation] Use a namespaced key strategy (e.g., `tracing.enabled`).
