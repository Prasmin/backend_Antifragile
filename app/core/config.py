from typing import Literal

from pydantic import PostgresDsn, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Represents the configuration settings for the application."""

    ENVIRONMENT: Literal["DEV", "PYTEST", "PREPROD", "PROD"] = "DEV"

    POSTGRES_SERVER: str = "localhost"  # non-sensitive, safe default
    POSTGRES_USER: str                  # required — must be set in .env
    POSTGRES_PASSWORD: str              # required — must be set in .env
    POSTGRES_PORT: int = 5432
    POSTGRES_DB: str                    # required — must be set in .env
    SQLALCHEMY_DATABASE_URI: PostgresDsn | None = None

    @model_validator(mode="after")
    def build_database_uri(self) -> "Settings":
        if self.SQLALCHEMY_DATABASE_URI is None:
            self.SQLALCHEMY_DATABASE_URI = PostgresDsn.build(
                scheme="postgresql+asyncpg",
                username=self.POSTGRES_USER,
                password=self.POSTGRES_PASSWORD,
                host=self.POSTGRES_SERVER,
                port=self.POSTGRES_PORT,
                path=self.POSTGRES_DB,
            )
        return self

    model_config = SettingsConfigDict(
        env_file=".env",          # load from .env file
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",           # ignore unknown env vars
    )


settings = Settings()  # type: ignore[call-arg]
