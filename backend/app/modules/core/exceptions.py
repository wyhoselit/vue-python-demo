class AuthException(Exception):
    def __init__(self, detail: str, error_code: str, status_code: int = 400):
        self.detail = detail
        self.error_code = error_code
        self.status_code = status_code
        super().__init__(detail)


class EmailAlreadyExistsError(AuthException):
    def __init__(self, detail: str = "Email already registered"):
        super().__init__(detail=detail, error_code="EMAIL_ALREADY_EXISTS", status_code=409)


class InvalidCredentialsError(AuthException):
    def __init__(self, detail: str = "Incorrect email or password"):
        super().__init__(detail=detail, error_code="INVALID_CREDENTIALS", status_code=401)


class ValidationError(AuthException):
    def __init__(self, detail: str = "Validation failed"):
        super().__init__(detail=detail, error_code="VALIDATION_ERROR", status_code=422)


class TokenExpiredError(AuthException):
    def __init__(self, detail: str = "Token has expired"):
        super().__init__(detail=detail, error_code="TOKEN_EXPIRED", status_code=401)