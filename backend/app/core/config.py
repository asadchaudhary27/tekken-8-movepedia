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

    # Cryptographic JWT & Security Settings
    JWT_SECRET_KEY: str = "43efbafec22418dce9a727050d62fb5bccded47fbdef6171919b8ab59a34d627"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440  # 24 hours

    # Initial SuperAdmin Credentials (read from .env on first seed)
    INITIAL_ADMIN_USER: str = "alpha"
    INITIAL_ADMIN_EMAIL: str = "asadqaisar17@gmail.com"
    INITIAL_ADMIN_PASSWORD: str = "Alpha_1122#"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

    @property
    def cors_origin_list(self) -> List[str]:
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",") if origin.strip()]


settings = Settings()
