from sqlalchemy import Column, Integer, String, JSON, DateTime
from sqlalchemy.sql import func
from app.modules.core.database import Base

class SystemSetting(Base):
    __tablename__ = "system_settings"

    id = Column(Integer, primary_key=True, index=True)
    key = Column(String, unique=True, index=True, nullable=False)
    settings = Column(JSON, nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    def __repr__(self) -> str:
        return f"<SystemSetting {self.key}>"
