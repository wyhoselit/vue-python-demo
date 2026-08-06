from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
import json

class CostTrackingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        
        # Only track AI endpoints
        if request.url.path.startswith("/api/v1/ai/"):
            # Example logic to track tokens from response body or headers
            # This is a simplified example. In reality, you'd integrate with
            # the LLM provider's response usage statistics.
            print(f"Tracking usage for: {request.url.path}")
            
        return response
