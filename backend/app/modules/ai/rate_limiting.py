from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from collections import defaultdict
import time

# Simple in-memory rate limiter for demonstration
rate_limits = defaultdict(list)

class RateLimitingMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, requests_per_minute=60):
        super().__init__(app)
        self.requests_per_minute = requests_per_minute

    async def dispatch(self, request: Request, call_next):
        if request.url.path.startswith("/api/v1/ai/"):
            user_id = request.headers.get("X-User-ID", "anonymous")
            now = time.time()
            
            # Filter requests within the last minute
            rate_limits[user_id] = [t for t in rate_limits[user_id] if t > now - 60]
            
            if len(rate_limits[user_id]) >= self.requests_per_minute:
                raise HTTPException(status_code=429, detail="Too many requests")
            
            rate_limits[user_id].append(now)
            
        return await call_next(request)
