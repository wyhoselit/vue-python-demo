from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.api.v1.deps import get_admin_user
from app.modules.core.database import get_db
from app.modules.system.services.setting_service import get_setting, set_setting, delete_setting

router = APIRouter()

@router.get("/config")
def get_tracing_config_api(
    admin=Depends(get_admin_user),
    db: Session = Depends(get_db)
):
    value = get_setting(db, "tracing.admin")
    return {"enabled": value.get("enabled", False) if value else False}

@router.put("/config")
def update_tracing_config(
    enabled: bool = Query(...),
    admin=Depends(get_admin_user),
    db: Session = Depends(get_db)
):
    set_setting(db, "tracing.admin", {"enabled": enabled})
    return {"enabled": enabled}
