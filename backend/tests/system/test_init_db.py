import pytest
import os
import secrets
from unittest.mock import patch, MagicMock, ANY
from sqlalchemy.orm import Session
from app.modules.system.models.system_setting import SystemSetting
from init_db import init_db, TOKEN_FILE

@patch("init_db.SessionLocal")
@patch("init_db.Base.metadata.create_all")
def test_init_db_seeds_token_from_file(mock_create_all, mock_session_local, tmp_path):
    """Test seeding token from existing .token file."""
    # Setup
    mock_db = MagicMock(spec=Session)
    mock_session_local.return_value = mock_db
    
    # Create .token file in tmp_path
    os.chdir(tmp_path)
    token_val = "existing-secret-token"
    with open(TOKEN_FILE, "w") as f:
        f.write(token_val)
    
    # Mock all DB queries to return None (settings don't exist yet)
    mock_db.query.return_value.filter.return_value.first.return_value = None
    
    init_db()
    
    # Verify - check that the last call to add was for the bearer token
    calls = mock_db.add.call_args_list
    bearer_token_added = False
    for call in calls:
        setting = call[0][0]
        if hasattr(setting, 'key') and setting.key == "system.default_bearer_token":
            bearer_token_added = True
            assert setting.settings == token_val
            break
    assert bearer_token_added, "Bearer token setting was not added"
    mock_db.commit.assert_called()

@patch("init_db.SessionLocal")
def test_init_db_generates_new_token(mock_session_local, tmp_path):
    """Test generation of new token if .token file missing."""
    # Setup
    mock_db = MagicMock(spec=Session)
    mock_session_local.return_value = mock_db
    os.chdir(tmp_path)
    
    if os.path.exists(TOKEN_FILE):
        os.remove(TOKEN_FILE)
    
    # Mock all DB queries to return None (settings don't exist yet)
    mock_db.query.return_value.filter.return_value.first.return_value = None
    
    init_db()
    
    # Verify file created and seeded
    assert os.path.exists(TOKEN_FILE)
    with open(TOKEN_FILE, "r") as f:
        token = f.read().strip()
        assert len(token) > 0
    
    # Find the bearer token setting in the calls
    calls = mock_db.add.call_args_list
    bearer_token_added = False
    for call in calls:
        setting = call[0][0]
        if hasattr(setting, 'key') and setting.key == "system.default_bearer_token":
            bearer_token_added = True
            assert setting.settings == token
            break
    assert bearer_token_added, "Bearer token setting was not added"