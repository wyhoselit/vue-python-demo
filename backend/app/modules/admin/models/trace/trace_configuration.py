"""Trace configuration model for enabling/disabling service tracing."""
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import Session
from app.modules.core.database import Base
from app.modules.system.services.setting_service import get_setting, set_setting

class TraceConfiguration(Base):
    """Trace configuration for individual services.

    Deprecated: Use SystemSetting instead.

    Attributes:
        id: Primary key identifier.
        service_name: Unique name of the service to trace.
    """

    __tablename__ = "trace_configurations"

    id = Column(Integer, primary_key=True, index=True)
    service_name = Column(String, unique=True, index=True, nullable=False)

    def get_enabled(self, db: Session) -> bool:
        """Check if tracing is enabled for this service.

        Args:
            db: Database session.

        Returns:
            True if tracing is enabled, False otherwise.
        """
        value = get_setting(db, f"tracing.{self.service_name}")
        return value.get("enabled", False) if value else False

    def set_enabled(self, db: Session, value: bool) -> None:
        """Enable or disable tracing for this service.

        Args:
            db: Database session.
            value: True to enable tracing, False to disable.
        """
        set_setting(db, f"tracing.{self.service_name}", {"enabled": value})

    def __repr__(self) -> str:
        """Return string representation of TraceConfiguration."""
        return f"<TraceConfiguration {self.service_name}>"

    def __init__(self, *args, **kwargs):
        import warnings
        warnings.warn("TraceConfiguration is deprecated. Use SystemSetting instead.", DeprecationWarning, stacklevel=2)
        super().__init__(*args, **kwargs)

def get_tracing_config(db_session: Session, service_name: str = "admin") -> TraceConfiguration:
    """Retrieve trace configuration for a service.

    Deprecated: TraceConfiguration table is now just a registry.

    Args:
        db_session: Database session.
        service_name: Name of the service to get config for.

    Returns:
        TraceConfiguration record or None if not found.
    """
    return db_session.query(TraceConfiguration).filter_by(service_name=service_name).first()
