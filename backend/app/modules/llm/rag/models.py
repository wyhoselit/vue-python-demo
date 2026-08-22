from sqlalchemy import Column, Integer, String, Text, JSON, DateTime, func
from pgvector.sqlalchemy import Vector
from app.modules.core.database import Base


class Document(Base):
    """RAG document model for storing processed documents.

    Attributes:
        id: Primary key identifier.
        content: Raw document content in text format.
        embedding: 384-dimensional vector embedding from sentence transformers.
        meta_data: Optional JSON metadata (source, chunk_id, etc.).
        created_at: Timestamp when document was indexed.
    """

    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text, nullable=False)
    embedding = Column(Vector(384), nullable=False)
    meta_data = Column(JSON, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    def __repr__(self) -> str:
        """Return string representation of Document."""
        return f"<Document {self.id}>"