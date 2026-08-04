import pytest
from fastapi import Request
from unittest.mock import Mock, patch
from app.api.v1.deps import extract_token_from_request, get_current_user
from app.modules.user.user import User
from sqlalchemy.orm import Session


def test_extract_token_from_request_with_bearer_token():
    """"Test Bearer token extraction from Authorization header"""
    mock_request = Mock(spec=Request)
    mock_request.headers.get.return_value = "Bearer test-token-123"
    mock_request.cookies = {}
    
    token = extract_token_from_request(mock_request)
    
    assert token == "test-token-123"
    mock_request.headers.get.assert_called_once_with("Authorization")


def test_extract_token_from_request_with_cookie():
    """"Test token extraction from cookie when no Bearer token"""
    mock_request = Mock(spec=Request)
    mock_request.headers.get.return_value = None
    mock_request.cookies = {"access_token": "cookie-token-456"}
    
    token = extract_token_from_request(mock_request)
    
    assert token == "cookie-token-456"


def test_extract_token_from_request_no_token():
    """Test when no token is available in header or cookie"""
    mock_request = Mock(spec=Request)
    mock_request.headers.get.return_value = None
    mock_request.cookies = {}
    
    token = extract_token_from_request(mock_request)
    
    assert token is None


def test_extract_token_from_request_bearer_without_prefix():
    """Test malformed Bearer token header (no prefix)"""
    mock_request = Mock(spec=Request)
    mock_request.headers.get.return_value = "test-token-no-prefix"
    mock_request.cookies = {}
    
    token = extract_token_from_request(mock_request)
    
    assert token is None


class MockUser:
    def __init__(self, id, username, email):
        self.id = id
        self.username = username
        self.email = email


def test_get_current_user_with_bearer_token(mock_db):
    """Test get_current_user with Bearer token authentication"""
    # Mock request with Bearer token
    mock_request = Mock(spec=Request)
    mock_request.headers.get.return_value = "Bearer bearer-token-123"
    mock_request.cookies = {}
    
    # Mock verify_token to return a valid payload
    with patch("app.api.v1.deps.verify_token") as mock_verify:
        mock_verify.return_value = {"sub": "1"}
        
        # Mock user query
        mock_user = MockUser(1, "bearer_user", "bearer@example.com")
        mock_db.query.return_value.filter.return_value.first.return_value = mock_user
        
        # Test that the function returns the user
        result = get_current_user(mock_request, mock_db)
        
        assert result == mock_user
        mock_verify.assert_called_once_with("bearer-token-123")


def test_get_current_user_with_cookie_auth(mock_db):
    """Test get_current_user with cookie-based authentication"""
    # Mock request with cookie
    mock_request = Mock(spec=Request)
    mock_request.headers.get.return_value = None
    mock_request.cookies = {"access_token": "cookie-token-456"}
    
    # Mock verify_token to return a valid payload
    with patch("app.api.v1.deps.verify_token") as mock_verify:
        mock_verify.return_value = {"sub": "2"}
        
        # Mock user query
        mock_user = MockUser(2, "cookie_user", "cookie@example.com")
        mock_db.query.return_value.filter.return_value.first.return_value = mock_user
        
        # Test that the function returns the user
        result = get_current_user(mock_request, mock_db)
        
        assert result == mock_user
        mock_verify.assert_called_once_with("cookie-token-456")


@pytest.fixture
def mock_db():
    """Mock database session fixture for testing"""
    return Mock(spec=Session)


def test_extract_token_precedence_bearer_over_cookie():
    """Test that Bearer token takes precedence over cookie"""
    mock_request = Mock(spec=Request)
    mock_request.headers.get.return_value = "Bearer bearer-token-123"
    mock_request.cookies = {"access_token": "cookie-token-456"}
    
    token = extract_token_from_request(mock_request)
    
    # Bearer token should be used, not cookie
    assert token == "bearer-token-123"