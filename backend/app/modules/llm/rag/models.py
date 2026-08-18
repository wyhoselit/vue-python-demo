from sqlalchemy import Column, Integer, String, Text, JSON, DateTime, func
from pgvector.sqlalchemy import Vector
from app.modules.core.database import Base


class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text, nullable=False)
    embedding = Column(Vector(384), nullable=False)
    meta_data = Column(JSON, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    def __repr__(self) -> str:
        return f"<Document {self.id}>"