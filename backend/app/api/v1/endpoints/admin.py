import sys
import platform
from fastapi import APIRouter, Depends
from app.api.v1.deps import get_admin_user
from app.core.database import get_db
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.models.user import User

router = APIRouter()

@router.get("/system-info")
def get_system_info(
    admin: User = Depends(get_admin_user),
    db: Session = Depends(get_db)
):
    db_status = "ok"
    try:
        db.execute(text("SELECT 1"))
    except:
        db_status = "error"
        
    return {
        "version": "1.0.0",
        "os": platform.platform(),
        "python": sys.version,
        "database": db_status
    }
