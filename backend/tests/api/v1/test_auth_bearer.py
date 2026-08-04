import pytest
from fastapi import Request
from app.api.v1.deps import extract_token_from_request

def test_extract_token_from_auth_header():
    """"Test token extraction from Authorization header."""
    # Use scope to correctly mock headers
    request = Request(scope={"type": "http", "headers": [(b"authorization", b"Bearer token123")]})
    token = extract_token_from_request(request)
    assert token == "token123"

def test_extract_token_from_auth_header_missing_bearer_prefix():
    """"Test token extraction fails without Bearer prefix."""
    request = Request(scope={"type": "http", "headers": [(b"authorization", b"token123")]})
    token = extract_token_from_request(request)
    assert token is None

def test_extract_token_from_cookie():
    """"Test token extraction from cookie when header not present."""
    request = Request(scope={"type": "http", "headers": [(b"cookie", b"access_token=cookie_token456")]})
    token = extract_token_from_request(request)
    assert token == "cookie_token456"

def test_extract_token_from_header_priority():
    """Test that Authorization header takes priority over cookie."""
    request = Request(scope={
        "type": "http", 
        "headers": [
            (b"authorization", b"Bearer header_token"),
            (b"cookie", b"access_token=cookie_token")
        ]
    })
    token = extract_token_from_request(request)
    assert token == "header_token"

def test_extract_token_no_token():
    """"Test token extraction when no token is present."""
    request = Request(scope={"type": "http", "headers": []})
    token = extract_token_from_request(request)
    assert token is None

def test_token_parsing_edge_cases():
    """Test malformed Authorization headers."""
    # Test empty header - "Bearer" without trailing space = None (not valid)
    request = Request(scope={"type": "http", "headers": [(b"authorization", b"Bearer")]})
    token = extract_token_from_request(request)
    assert token is None
    
    # Test malformed header (extra space)
    request = Request(scope={"type": "http", "headers": [(b"authorization", b"Bearer token  ")]})
    token = extract_token_from_request(request)
    assert token == "token  "
    
    # Test token with special characters
    request = Request(scope={"type": "http", "headers": [(b"authorization", b"Bearer token!@#$%")]})
    token = extract_token_from_request(request)
    assert token == "token!@#$%"
