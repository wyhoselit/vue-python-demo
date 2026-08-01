import pytest
import os
from app.modules.core.config import Settings, settings


class TestSettings:
    def test_settings_has_database_url(self):
        assert hasattr(settings, "DATABASE_URL")
        assert isinstance(settings.DATABASE_URL, str)

    def test_settings_has_secret_key(self):
        assert hasattr(settings, "SECRET_KEY")
        assert isinstance(settings.SECRET_KEY, str)

    def test_settings_has_debug(self):
        assert hasattr(settings, "DEBUG")
        assert isinstance(settings.DEBUG, bool)

    def test_settings_has_cors_origins(self):
        assert hasattr(settings, "CORS_ORIGINS")
        assert isinstance(settings.CORS_ORIGINS, str)

    def test_settings_has_api_v1_prefix(self):
        assert hasattr(settings, "API_V1_PREFIX")
        assert isinstance(settings.API_V1_PREFIX, str)

    def test_database_url_default(self):
        test_settings = Settings()
        assert test_settings.DATABASE_URL == "sqlite:///./app.db"

    def test_secret_key_default(self):
        test_settings = Settings()
        assert test_settings.SECRET_KEY == "change-me-in-production"

    def test_debug_default(self):
        test_settings = Settings()
        assert test_settings.DEBUG is False

    def test_cors_origins_default(self):
        test_settings = Settings()
        assert test_settings.CORS_ORIGINS == "http://localhost:5173"

    def test_api_v1_prefix_default(self):
        test_settings = Settings()
        assert test_settings.API_V1_PREFIX == "/api/v1"

    def test_settings_with_env_override(self, monkeypatch):
        monkeypatch.setenv("DEBUG", "true")
        test_settings = Settings()
        assert test_settings.DEBUG is True

    def test_settings_creates_instance(self):
        test_settings = Settings()
        assert isinstance(test_settings, Settings)