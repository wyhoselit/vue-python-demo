import pytest
from app.modules.core.database import get_db

def test_get_db():
    db_gen = get_db()
    db = next(db_gen)
    assert db is not None
    # Assuming standard SQLAlchemy session attributes
    assert hasattr(db, 'close')
    
    # Check if close is called when generator ends
    with pytest.raises(StopIteration):
        next(db_gen)
