import pytest

from app.modules.core.config import Settings


def test_default_settings():
    settings = Settings(_env_file=None)
    assert settings.DEBUG is False
    assert settings.CORS_ORIGINS == "http://localhost:5173"
    assert settings.API_V1_PREFIX == "/api/v1"


def test_settings_has_required_fields():
    settings = Settings()
    assert hasattr(settings, 'DATABASE_URL')
    assert hasattr(settings, 'SECRET_KEY')
    assert hasattr(settings, 'DEBUG')
    assert hasattr(settings, 'CORS_ORIGINS')
    assert hasattr(settings, 'API_V1_PREFIX')


def test_database_url_default():
    settings = Settings(_env_file=None)
    assert settings.DATABASE_URL == "sqlite:///./app.db"