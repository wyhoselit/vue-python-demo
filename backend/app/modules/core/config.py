from pydantic_settings import BaseSettings, SettingsConfigDict


import os

class Settings(BaseSettings):
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./app.db")
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    SECRET_KEY: str = os.getenv("SECRET_KEY", "change-me-in-production")
    DEBUG: bool = False
    CORS_ORIGINS: str = os.getenv("CORS_ORIGINS", "http://localhost:5173")
    API_V1_PREFIX: str = "/api/v1"
    LOG_FILE_PATH: str = os.getenv("LOG_FILE_PATH", "/app/logs/server.log")

    model_config = SettingsConfigDict(env_file=".env", case_sensitive=True, extra='ignore')


settings = Settings()
