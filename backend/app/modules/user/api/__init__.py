from app.modules.admin.api.status import router as status_router
from app.modules.admin.api.logs import router as logs_router
from app.modules.admin.api.tracing import router as tracing_router
from app.modules.user.api.auth.auth import router as auth_router
from app.modules.dashboard.api.dashboard import router as dashboard_router
from app.modules.system.api.health import router as health_router

__all__ = [
    "status_router",
    "logs_router",
    "tracing_router",
    "auth_router",
    "dashboard_router",
    "health_router",
]