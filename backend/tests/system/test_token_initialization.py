import pytest
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

import pytest
from app.modules.system.models.system_setting import SystemSetting
from app.modules.core.database import Base, SessionLocal, engine
from init_db import init_db

def test_token_initialization_from_file(tmp_path):
    """Test that system.default_bearer_token is seeded from .token file during migration."""
    
    # Create a temporary database
    temp_db_path = tmp_path / "test.db"
    
    # Mock engine connection
    import app.modules.core.database
    app.modules.core.database.engine = engine.execution_options(schema_translate_map={None: "main"})
    
    # Set up test DB
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    
    # Create test .token file
    token_file = tmp_path / ".token"
    test_token = "test-admin-token"
    token_file.write_text(test_token)
    
    # Change working directory to tmp_path so init_db finds .token
    original_cwd = os.getcwd()
    os.chdir(tmp_path)
    
    try:
        # Initialize DB
        init_db()
        
        # Check that token was seeded
        setting = db.query(SystemSetting).filter(SystemSetting.key == "system.default_bearer_token").first()
        assert setting is not None
        assert setting.settings == test_token
    finally:
        os.chdir(original_cwd)
        db.close()
        Base.metadata.drop_all(bind=engine)
