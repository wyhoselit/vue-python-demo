from fastapi import APIRouter, Depends, Body, HTTPException
from sqlalchemy.orm import Session
from app.api.v1.deps import get_admin_user
from app.modules.core.database import get_db
from app.modules.system.services.setting_service import get_setting, set_setting, sync_token_to_file, get_all_settings
from app.modules.system.models.system_setting import SystemSetting
from typing import Any
import os

TOKEN_FILE = ".token"

router = APIRouter()

@router.get("/")
def get_all_configs(
    admin=Depends(get_admin_user),
    db: Session = Depends(get_db)
):
    return get_all_settings(db)

@router.get("/{key}")
def get_config(
    key: str,
    admin=Depends(get_admin_user),
    db: Session = Depends(get_db)
):
    value = get_setting(db, key)
    
    # Sync token from file if reading default bearer token
    if key == "system.default_bearer_token":
        db_token = value or ""
        file_token = ""
        if os.path.exists(TOKEN_FILE):
            try:
                with open(TOKEN_FILE, "r") as f:
                    file_token = f.read().strip()
            except Exception:
                pass
        
        # If file has token but db doesn't, update db
        if file_token and file_token != db_token:
            set_setting(db, key, file_token)
            value = file_token
    
    return value

@router.put("/{key}")
def update_config(
    key: str,
    payload: dict = Body(...),
    admin=Depends(get_admin_user),
    db: Session = Depends(get_db)
):
    if "value" not in payload:
        raise HTTPException(status_code=422, detail="Value is required in payload")
    
    value = payload["value"]
        
    setting = db.query(SystemSetting).filter(SystemSetting.key == key).first()
    if not setting:
        raise HTTPException(status_code=404, detail="Setting not found")
        
    set_setting(db, key, value)
    
    # Sync token to file if writing default bearer token
    if key == "system.default_bearer_token":
        sync_token_to_file(value)
    
    return {"key": key, "value": value}
