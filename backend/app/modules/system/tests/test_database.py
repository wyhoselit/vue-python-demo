import pytest
from sqlalchemy import text
from sqlalchemy import create_engine

from app.modules.core.database import engine, get_db, Base, SessionLocal
from app.modules.core.config import settings


@pytest.fixture(scope="module")
def setup_test_db(request):
    original_database_url = settings.DATABASE_URL
    settings.DATABASE_URL = "sqlite:///./test_temp.db"
    
    # Use the test engine defined in conftest.py
    # or create a temporary one here if not using conftest's engine
    test_engine = create_engine(settings.DATABASE_URL, connect_args={"check_same_thread": False})
    Base.metadata.create_all(bind=test_engine)
    
    def teardown():
        Base.metadata.drop_all(bind=test_engine)
        settings.DATABASE_URL = original_database_url
    request.addfinalizer(teardown)


def test_database_connection():
    with engine.connect() as connection:
        result = connection.execute(text("SELECT 1"))
        assert result.scalar() == 1


def test_get_db_dependency():
    gen = get_db()
    db = next(gen)
    assert db is not None
    # Verify session is still open while in use
    assert db.is_active
    # Close session via generator
    with pytest.raises(StopIteration):
        next(gen)
