from .admin.status import router as status_router
from .admin.logs import router as logs_router
from .admin.tracing import router as tracing_router
from .auth.auth import router as auth_router
from .dashboard.dashboard import router as dashboard_router
from .health.health import router as health_router

__all__ = [
    "status_router",
    "logs_router",
    "tracing_router",
    "auth_router",
    "dashboard_router",
    "health_router",
]