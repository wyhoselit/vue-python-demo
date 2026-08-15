import os
import pytest
from starlette.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Setup test env before importing app
os.environ["LOG_FILE_PATH"] = "./test.log"

from app.modules.core.config import settings
from app.modules.core.database import Base, get_db

# Import the main app function to create a new app instance for each test
from app.main import create_app
from app.modules.core.observability import setup_observability

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
test_engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)

@pytest.fixture(name="session", scope="function")
def session_fixture():
    Base.metadata.drop_all(bind=test_engine)
    Base.metadata.create_all(bind=test_engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture(name="db")
def db_fixture(session):
    yield session


@pytest.fixture(name="client", scope="function")
def client_fixture(session):
    def get_session_override():
        return session

    app = create_app(lifespan=None)
    setup_observability(app)
    app.dependency_overrides[get_db] = get_session_override
    
    with TestClient(app) as client:
        yield client
        
    app.dependency_overrides.clear()
