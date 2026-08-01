from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api.v1.deps import get_admin_user
from app.core.database import get_db
from app.modules.admin.models.trace.trace_configuration import TraceConfiguration, get_tracing_config

router = APIRouter()

@router.get("/config")
def get_tracing_config_api(
    admin=Depends(get_admin_user),
    db: Session = Depends(get_db)
):
    config = get_tracing_config(db)
    return {"enabled": config.enabled if config else False}

@router.put("/config")
def update_tracing_config(
    enabled: bool,
    admin=Depends(get_admin_user),
    db: Session = Depends(get_db)
):
    config = get_tracing_config(db)
    if not config:
        config = TraceConfiguration(service_name="admin", enabled=enabled)
        db.add(config)
    else:
        config.enabled = enabled
    db.commit()
    db.refresh(config)
    return {"enabled": config.enabled}
