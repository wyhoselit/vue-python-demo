from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship, Session
from app.core.database import Base

class TraceConfiguration(Base):
    __tablename__ = "trace_configurations"

    id = Column(Integer, primary_key=True, index=True)
    service_name = Column(String, unique=True, index=True, nullable=False)
    enabled = Column(Boolean, default=False)
    
    def save(self) -> None:
        db = Session.object_session(self)
        if db:
            db.add(self)
            db.commit()
            db.refresh(self)
    
    def __repr__(self) -> str:
        return f"<TraceConfiguration {self.service_name}={self.enabled}>"

def get_tracing_config(db_session: Session, service_name: str = "admin") -> TraceConfiguration:
    return db_session.query(TraceConfiguration).filter_by(service_name=service_name).first()
