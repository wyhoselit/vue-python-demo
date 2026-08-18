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
    OTEL_COLLECTOR_ENDPOINT: str = os.getenv("OTEL_COLLECTOR_ENDPOINT", "otel-collector:4317")
    OTEL_COLLECTOR_HTTP_ENDPOINT: str = os.getenv("OTEL_COLLECTOR_HTTP_ENDPOINT", "http://otel-collector:4318")
    SERVICE_NAME: str = os.getenv("SERVICE_NAME", "backend-service")

    VECTOR_STORE: str = os.getenv("VECTOR_STORE", "chroma")
    PGVECTOR_HNSW_M: int = int(os.getenv("PGVECTOR_HNSW_M", "16"))
    PGVECTOR_HNSW_EF_CONSTRUCTION: int = int(os.getenv("PGVECTOR_HNSW_EF_CONSTRUCTION", "64"))

    model_config = SettingsConfigDict(env_file=".env", case_sensitive=True, extra='ignore')


settings = Settings()
