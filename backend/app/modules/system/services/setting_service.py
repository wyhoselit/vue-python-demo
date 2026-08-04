import os
from sqlalchemy.orm import Session
from app.modules.system.models.system_setting import SystemSetting
from typing import Any, Optional

TOKEN_FILE = ".token"

def get_setting(db_session: Session, key: str) -> Optional[Any]:
    setting = db_session.query(SystemSetting).filter(SystemSetting.key == key).first()
    return setting.settings if setting else None

def set_setting(db_session: Session, key: str, value: Any) -> None:
    setting = db_session.query(SystemSetting).filter(SystemSetting.key == key).first()
    if setting:
        setting.settings = value
    else:
        setting = SystemSetting(key=key, settings=value)
        db_session.add(setting)
    db_session.commit()

def sync_token_to_file(token: str) -> None:
    try:
        with open(TOKEN_FILE, "w") as f:
            f.write(token)
    except Exception as e:
        print(f"Error writing to {TOKEN_FILE}: {e}")

def delete_setting(db_session: Session, key: str) -> None:
    setting = db_session.query(SystemSetting).filter(SystemSetting.key == key).first()
    if setting:
        db_session.delete(setting)
        db_session.commit()
