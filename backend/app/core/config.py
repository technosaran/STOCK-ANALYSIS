from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_name: str = "QuantEdge API"
    api_version: str = "0.1.0"

    secret_key: str = Field("change-me-in-prod", min_length=16)
    access_token_expire_minutes: int = 30
    refresh_token_expire_minutes: int = 60 * 24 * 7
    algorithm: str = "HS256"

    postgres_url: str = "sqlite+pysqlite:///./quantedge.db"
    redis_url: str = "redis://localhost:6379/0"

    yahoo_cache_ttl_seconds: int = 300
    auth_rate_limit_per_minute: int = 20


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
