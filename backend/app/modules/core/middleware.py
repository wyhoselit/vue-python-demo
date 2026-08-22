"""HTTP middleware components for request handling.

Includes tracing, logging, and security-related middlewares.
"""
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
import uuid

class RequestIDMiddleware(BaseHTTPMiddleware):
    """Middleware to inject a unique Request ID into each request and response header."""
    async def dispatch(self, request: Request, call_next):
        """Handle incoming request and add Request ID.

        Args:
            request: Incoming HTTP request.
            call_next: Next request handler in chain.

        Returns:
            HTTP response with X-Request-ID header.
        """
        request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))
        request.state.request_id = request_id
        response = await call_next(request)
        response.headers["X-Request-ID"] = request_id
        return response