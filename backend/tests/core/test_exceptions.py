import pytest
from app.core.exceptions import (
    AuthException,
    EmailAlreadyExistsError,
    InvalidCredentialsError,
    ValidationError,
    TokenExpiredError
)


class TestAuthException:
    def test_auth_exception_initialization(self):
        exception = AuthException("Test detail", "test_error", 400)
        assert exception.detail == "Test detail"
        assert exception.error_code == "test_error"
        assert exception.status_code == 400
        assert "Test detail" in str(exception)

    def test_auth_exception_with_error_code(self):
        exception = AuthException("Test detail", "test_error", 400)
        assert exception.detail == "Test detail"
        assert exception.error_code == "test_error"
        assert exception.status_code == 400


class TestEmailAlreadyExistsError:
    def test_email_already_exists_default_detail(self):
        exception = EmailAlreadyExistsError()
        assert exception.detail == "Email already registered"
        assert exception.error_code == "EMAIL_ALREADY_EXISTS"
        assert exception.status_code == 409

    def test_email_already_exists_custom_detail(self):
        exception = EmailAlreadyExistsError("Custom message")
        assert exception.detail == "Custom message"
        assert exception.error_code == "EMAIL_ALREADY_EXISTS"
        assert exception.status_code == 409

    def test_email_already_exists_inheritance(self):
        exception = EmailAlreadyExistsError()
        assert isinstance(exception, AuthException)


class TestInvalidCredentialsError:
    def test_invalid_credentials_default_detail(self):
        exception = InvalidCredentialsError()
        assert exception.detail == "Incorrect email or password"
        assert exception.error_code == "INVALID_CREDENTIALS"
        assert exception.status_code == 401

    def test_invalid_credentials_custom_detail(self):
        exception = InvalidCredentialsError("Wrong credentials")
        assert exception.detail == "Wrong credentials"
        assert exception.error_code == "INVALID_CREDENTIALS"
        assert exception.status_code == 401

    def test_invalid_credentials_inheritance(self):
        exception = InvalidCredentialsError()
        assert isinstance(exception, AuthException)


class TestValidationError:
    def test_validation_error_default_detail(self):
        exception = ValidationError()
        assert exception.detail == "Validation failed"
        assert exception.error_code == "VALIDATION_ERROR"
        assert exception.status_code == 422

    def test_validation_error_custom_detail(self):
        exception = ValidationError("Custom validation error")
        assert exception.detail == "Custom validation error"
        assert exception.error_code == "VALIDATION_ERROR"
        assert exception.status_code == 422

    def test_validation_error_inheritance(self):
        exception = ValidationError()
        assert isinstance(exception, AuthException)


class TestTokenExpiredError:
    def test_token_expired_default_detail(self):
        exception = TokenExpiredError()
        assert exception.detail == "Token has expired"
        assert exception.error_code == "TOKEN_EXPIRED"
        assert exception.status_code == 401

    def test_token_expired_custom_detail(self):
        exception = TokenExpiredError("Expired please re-login")
        assert exception.detail == "Expired please re-login"
        assert exception.error_code == "TOKEN_EXPIRED"
        assert exception.status_code == 401

    def test_token_expired_inheritance(self):
        exception = TokenExpiredError()
        assert isinstance(exception, AuthException)

    def test_all_exceptions_inheritance_from_auth_exception(self):
        exceptions = [
            EmailAlreadyExistsError(),
            InvalidCredentialsError(),
            ValidationError(),
            TokenExpiredError()
        ]
        for exc in exceptions:
            assert isinstance(exc, AuthException)