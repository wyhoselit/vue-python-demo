# System Config Management Spec

## Summary
A centralized system configuration API to manage all system-wide settings from a single interface.

## Requirements

### GET /api/v1/system/config

**When**
- Admin requests a list of all system settings via the centralized configuration API

**Then**
- Return a JSON map of all key-value pairs from the `system_settings` table
- Each entry contains:
  - Key: System setting identifier (e.g., `system.logfile_path`, `system.tracing`)
  - Value: Setting value based on stored type (string, boolean, number, JSON)

**Then**
- Return 200 OK with complete settings map

### PUT /api/v1/system/config/{key}

**When**
- Admin requests to update a specific system setting via the centralized configuration API

**Then**
- Validate admin authentication
- Update the setting in the `system_settings` table with new value
- Return confirmation of update

**Payload**
```json
{
  "value": "new value"
}
```

**Then**
- Return 200 OK with:
  - `key`: Updated setting key
  - `value`: New value

## Technical Specifications

### API Endpoint
- **GET**: `/api/v1/system/config`
- **PUT**: `/api/v1/system/config/{key}`

### Authentication
- Bearer token authentication via `Authorization` header
- Admin-level permissions required

### Data Model
- Uses existing `system_settings` table with `key` and `settings` fields
- Settings stored as JSON to support different data types
- Dynamic form controls based on stored data type

### Request/Response Models

**GET /api/v1/system/config Response**
```json
{
  "system.logfile_path": {
    "type": "string",
    "value": "/var/log/app.log",
    "description": "Application logfile path"
  },
  "system.tracing": {
    "type": "boolean",
    "value": false,
    "description": "Enable application tracing"
  }
}
```

**PUT /api/v1/system/config/{key} Response**
```json
{
  "key": "system.logfile_path",
  "value": "/var/log/new.log",
  "type": "string"
}
```

## Frontend Integration

### API Requests

**List All Settings**
```javascript
const response = await api.get('/api/v1/system/config');
const settings = response.data;
```

**Update Setting**
```javascript
const response = await api.put('/api/v1/system/config/{key}', {
  value: "new value"
});
```

### Dynamic Form Rendering

The frontend will dynamically generate form controls based on:
- Boolean values: Toggle switches
- String values: Text inputs
- Number values: Number inputs
- JSON objects: Advanced editor components

### Validation
- Client-side validation based on expected type
- Server-side validation in the API

## Error Handling

### GET /api/v1/system/config
- **403**: No admin permissions
- **500**: Internal server error

### PUT /api/v1/system/config/{key}
- **400**: Invalid payload format
- **403**: No admin permissions
- **404**: Setting not found
- **500**: Internal server error

## Security Considerations

- Admin authentication required for all endpoints
- Input validation to prevent injection attacks
- Rate limiting for configuration updates
- Audit logging for configuration changes

## Testing

### Backend Tests
- Verify endpoint authentication
- Test all CRUD operations
- Validate error conditions

### Frontend Tests
- Component renders with settings data
- Dynamic control generation based on type
- Update operations success scenarios
- Error handling displays

## Migration Considerations

- **Existing endpoints**: `/api/v1/system/config/{key}` is consolidated from module-specific endpoints
- **Frontend changes**: Migration from individual endpoints to centralized API
- **Backward compatibility**: Existing tracing and logfile path settings continue to work with new unified API