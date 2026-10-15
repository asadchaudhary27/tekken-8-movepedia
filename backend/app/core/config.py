import os
from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_NAME: str = "Tekken 8 Movepedia & Training Assistant"
    APP_VERSION: str = "1.0.0-phase1"
    APP_ENV: str = "development"
    DEBUG: bool = True
    API_V1_PREFIX: str = "/api/v1"
    HOST: str = "127.0.0.1"
    PORT: int = 8000

    # Database
    DATABASE_URL: str = "sqlite:///./tekken8_fyp.db"

    # Ingestion & Network
    REQUEST_TIMEOUT_SECONDS: int = 15
    MAX_RETRIES: int = 3
    RATE_LIMIT_DELAY_SECONDS: float = 1.0

    # CORS
    CORS_ORIGINS: str = "http://localhost:8000,http://127.0.0.1:8000,http://localhost:3000,*"

    # Admin & Game Patch Defaults
    ADMIN_SECRET_KEY: str = "tekken8-fyp-admin-secret-2026"
    CURRENT_GAME_PATCH: str = "3.00.02"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

    @property
    def cors_origin_list(self) -> List[str]:
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",") if origin.strip()]


settings = Settings()
