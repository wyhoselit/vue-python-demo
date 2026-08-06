from sqlalchemy import Column, Integer, String, JSON, DateTime
from datetime import datetime
from backend.app.modules.core.database import Base

class ModelRegistry(Base):
    __tablename__ = "model_registry"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    version = Column(String, index=True)
    metadata_json = Column(JSON)  # Store config/metadata
    created_at = Column(DateTime, default=datetime.utcnow)

    def __init__(self, name: str, version: str, metadata: dict):
        self.name = name
        self.version = version
        self.metadata_json = metadata
