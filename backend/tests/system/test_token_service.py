import os
import pytest
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from app.modules.system.services.setting_service import sync_token_to_file

TOKEN_FILE = ".token"

def test_sync_token_to_file():
    token = "test-token-123"
    sync_token_to_file(token)
    
    assert os.path.exists(TOKEN_FILE)
    with open(TOKEN_FILE, "r") as f:
        assert f.read().strip() == token
    
    # Cleanup
    os.remove(TOKEN_FILE)
