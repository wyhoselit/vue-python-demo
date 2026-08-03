from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import Session
from app.modules.core.database import Base
from app.modules.system.services.setting_service import get_setting, set_setting

class TraceConfiguration(Base):
    __tablename__ = "trace_configurations"

    id = Column(Integer, primary_key=True, index=True)
    service_name = Column(String, unique=True, index=True, nullable=False)
    
    def get_enabled(self, db: Session) -> bool:
        value = get_setting(db, f"tracing.{self.service_name}")
        return value.get("enabled", False) if value else False
    
    def set_enabled(self, db: Session, value: bool) -> None:
        set_setting(db, f"tracing.{self.service_name}", {"enabled": value})
    
    def __repr__(self) -> str:
        return f"<TraceConfiguration {self.service_name}>"

    def __init__(self, *args, **kwargs):
        import warnings
        warnings.warn("TraceConfiguration is deprecated. Use SystemSetting instead.", DeprecationWarning, stacklevel=2)
        super().__init__(*args, **kwargs)

def get_tracing_config(db_session: Session, service_name: str = "admin") -> TraceConfiguration:
    # Deprecated: TraceConfiguration table is now just a registry.
    return db_session.query(TraceConfiguration).filter_by(service_name=service_name).first()
