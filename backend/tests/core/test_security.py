import pytest
from datetime import timedelta
from app.core.security import hash_password, verify_password, create_access_token, verify_token
from app.core.config import settings


class TestHashPassword:
    def test_hash_password_returns_string(self):
        password = "testpassword123"
        result = hash_password(password)
        assert isinstance(result, str)
    
    def test_hash_password_creates_different_hashes(self):
        password = "testpassword123"
        hash1 = hash_password(password)
        hash2 = hash_password(password)
        assert hash1 != hash2
    
    def test_hash_password_is_bcrypt_format(self):
        password = "testpassword123"
        result = hash_password(password)
        assert result.startswith("$2b$")


class TestVerifyPassword:
    def test_verify_password_correct(self):
        password = "testpassword123"
        hashed = hash_password(password)
        assert verify_password(password, hashed) is True
    
    def test_verify_password_incorrect(self):
        password = "testpassword123"
        hashed = hash_password(password)
        assert verify_password("wrongpassword", hashed) is False
    
    def test_verify_password_empty(self):
        hashed = hash_password("testpassword123")
        assert verify_password("", hashed) is False


class TestCreateAccessToken:
    def test_create_access_token_returns_string(self):
        data = {"sub": "testuser"}
        result = create_access_token(data)
        assert isinstance(result, str)
    
    def test_create_access_token_includes_expiry(self):
        data = {"sub": "testuser"}
        result = create_access_token(data)
        payload = verify_token(result)
        assert payload is not None
        assert "exp" in payload
    
    def test_create_access_token_custom_expiry(self):
        data = {"sub": "testuser"}
        result = create_access_token(data, expires_delta=timedelta(hours=1))
        payload = verify_token(result)
        assert payload is not None
        assert payload["sub"] == "testuser"


class TestVerifyToken:
    def test_verify_token_valid(self):
        data = {"sub": "testuser"}
        token = create_access_token(data)
        payload = verify_token(token)
        assert payload is not None
        assert payload["sub"] == "testuser"
    
    def test_verify_token_invalid(self):
        payload = verify_token("invalid.token.here")
        assert payload is None
    
    def test_verify_token_empty(self):
        payload = verify_token("")
        assert payload is None