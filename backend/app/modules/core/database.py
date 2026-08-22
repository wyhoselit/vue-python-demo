"""Database connection and session management.

Provides the SQLAlchemy engine, session factory, and declarative base
used by all application models.
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.modules.core.config import settings

connect_args = {}
engine_kwargs = {}

if settings.DATABASE_URL.startswith("sqlite"):
    connect_args["check_same_thread"] = False
else:
    engine_kwargs.update({
        "pool_size": 10,
        "max_overflow": 20,
        "pool_recycle": 3600,
        "pool_pre_ping": True,
    })

engine = create_engine(
    settings.DATABASE_URL,
    connect_args=connect_args,
    **engine_kwargs
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    """Provide a transactional database session.

    Yields:
        Session: SQLAlchemy database session.

    The session is automatically closed when the request completes.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
