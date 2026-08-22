"""Trace entry model for performance monitoring."""
from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.sql import func
from app.modules.core.database import Base

class TraceEntry(Base):
    """Performance trace entry for function execution.

    Attributes:
        id: Primary key identifier.
        function_name: Name of traced function.
        module_name: Module where function resides.
        duration: Execution time in seconds.
        timestamp: When trace was recorded.
    """

    __tablename__ = "trace_entries"

    id = Column(Integer, primary_key=True, index=True)
    function_name = Column(String, index=True, nullable=False)
    module_name = Column(String, index=True, nullable=False)
    duration = Column(Float, nullable=False)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())

    def __repr__(self) -> str:
        """Return string representation of TraceEntry."""
        return f"<TraceEntry {self.module_name}.{self.function_name} {self.duration}s>"
