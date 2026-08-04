from fastapi import APIRouter
from app.api.versioning import APIVersion
from app.api.version_router import register_version, get_router_for_version
from app.modules.system.api.health import router as health_router
from app.modules.system.api.config import router as system_config_router
from app.modules.user.api.auth.auth import router as auth_router
from app.modules.admin.api.status import router as admin_status_router
from app.modules.admin.api.logs import router as admin_logs_router
from app.modules.dashboard.api.dashboard import router as dashboard_router
from app.modules.user.api.users import router as user_router

api_router = APIRouter()

# Versioned routers
v1_router = APIRouter()
v2_router = APIRouter()

# v1 routes
v1_router.include_router(health_router, prefix="/health", tags=["health"])
v1_router.include_router(system_config_router, prefix="/system/config", tags=["system"])
v1_router.include_router(auth_router, prefix="/auth", tags=["auth"])
v1_router.include_router(admin_status_router, prefix="/admin", tags=["admin"])
v1_router.include_router(admin_logs_router, prefix="/admin", tags=["admin"])
v1_router.include_router(dashboard_router, prefix="/dashboard", tags=["dashboard"])
v1_router.include_router(user_router, prefix="/users", tags=["users"])

# v2 routes
v2_router.include_router(health_router, prefix="/health", tags=["health"])
v2_router.include_router(auth_router, prefix="/auth", tags=["auth"])
v2_router.include_router(admin_status_router, prefix="/admin", tags=["admin"])
v2_router.include_router(admin_logs_router, prefix="/admin", tags=["admin"])
v2_router.include_router(dashboard_router, prefix="/dashboard", tags=["dashboard"])
v2_router.include_router(user_router, prefix="/users", tags=["users"])

# Register versioned routers
register_version(APIVersion.V1, v1_router)
register_version(APIVersion.V2, v2_router)

# Include versioned routers
api_router.include_router(get_router_for_version(APIVersion.V1), prefix="/v1")
api_router.include_router(get_router_for_version(APIVersion.V2), prefix="/v2")
