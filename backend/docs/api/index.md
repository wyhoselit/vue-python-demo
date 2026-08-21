# API Reference

## Endpoints

All API endpoints are organized under `/api/v1` and `/api/v2` prefixes.

### Authentication

Most endpoints require authentication via Bearer token:

```
Authorization: Bearer <access_token>
```

### Rate Limiting

AI endpoints have rate limiting applied.

### Error Responses

All endpoints follow a consistent error format:

```json
{
  "detail": "Error description",
  "error_code": "ERROR_CODE"
}
```

## Endpoint Categories

| Category | Path | Description |
|----------|------|-------------|
| Health | `/api/health` | System health check |
| Auth | `/api/v1/auth/*` | Login, registration, token refresh |
| Users | `/api/v1/users/*` | User management |
| AI Chat | `/api/v1/ai/chat` | Chat completion |
| AI RAG | `/api/v1/ai/rag_chat` | RAG chat completion |
| Embeddings | `/api/v1/ai/embeddings` | Text embeddings |
| Admin | `/api/v1/admin/*` | Admin functions |

## Interactive Documentation

FastAPI provides built-in interactive docs:
- Swagger UI: `/docs`
- ReDoc: `/redoc`