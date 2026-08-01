from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.sql import func
from app.modules.core.database import Base

class TraceEntry(Base):
    __tablename__ = "trace_entries"

    id = Column(Integer, primary_key=True, index=True)
    function_name = Column(String, index=True, nullable=False)
    module_name = Column(String, index=True, nullable=False)
    duration = Column(Float, nullable=False)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    
    def __repr__(self) -> str:
        return f"<TraceEntry {self.module_name}.{self.function_name} {self.duration}s>"
