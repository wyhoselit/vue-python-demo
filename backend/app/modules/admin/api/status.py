"""Admin system status API endpoints."""
import platform
from fastapi import APIRouter, Depends
from app.api.v1.deps import get_admin_user
from app.modules.core.database import get_db
from sqlalchemy.orm import Session

router = APIRouter()

@router.get("/system-info")
def get_admin_system_info(
    admin=Depends(get_admin_user),
    db: Session = Depends(get_db)
):
    """Retrieve system information for admin monitoring.

    Args:
        admin: Dependency to verify admin user privileges.
        db: Database session for potential future use.

    Returns:
        System status information including health status, version, OS, and database type.
    """
    return {
        "status": "ok",
        "version": "0.1.0",
        "os": platform.system(),
        "database": "sqlite"
    }


