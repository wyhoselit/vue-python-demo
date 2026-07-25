from fastapi import APIRouter

from app.api.v1.endpoints import health, dashboard, users

api_router = APIRouter()

api_router.include_router(health.router, prefix="/health", tags=["health"])
api_router.include_router(dashboard.router, prefix="/dashboard", tags=["dashboard"])
api_router.include_router(users.router, prefix="/users", tags=["users"])