from fastapi import APIRouter

from app.modules.admin.api.status import router as admin_router
from app.modules.admin.api.logs import router as logs_router
from app.modules.admin.api.tracing import router as tracing_router
from app.modules.user.api.auth.auth import router as auth_router
from app.modules.dashboard.api.dashboard import router as dashboard_router
from app.modules.system.api.health import router as health_router
from app.modules.user.api.users import router as users_router

api_router = APIRouter()

api_router.include_router(health_router, prefix="/health", tags=["health"])
api_router.include_router(dashboard_router, prefix="/dashboard", tags=["dashboard"])
api_router.include_router(users_router, prefix="/users", tags=["users"])
api_router.include_router(auth_router, prefix="/auth", tags=["auth"])
api_router.include_router(admin_router, prefix="/admin", tags=["admin"])
api_router.include_router(logs_router, prefix="/admin", tags=["admin"])
api_router.include_router(tracing_router, prefix="/admin/tracing", tags=["admin"])