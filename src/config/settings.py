"""Typed application settings loaded from environment variables."""

from functools import lru_cache
from pathlib import Path
from typing import Annotated, Literal

from pydantic import AliasChoices, Field, field_validator
from pydantic_settings import BaseSettings, NoDecode, SettingsConfigDict


class AppSettings(BaseSettings):
    """Environment-backed runtime configuration for the application."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    app_env: Literal["development", "test", "production"] = "development"
    app_host: str = "0.0.0.0"
    app_port: int = Field(default=8000, ge=1, le=65535)
    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = "INFO"

    music_source_roots: Annotated[list[Path], NoDecode] = Field(
        default_factory=list,
        validation_alias=AliasChoices("MUSIC_SOURCE_ROOTS", "MUSIC_SOURCE_ROOT"),
    )
    tagged_output_root: Path = Path("./tagged-output")
    clear_metadata: bool = False

    musicbrainz_user_agent: str = "pytagrelease/0.1.0 (contact: you@example.com)"
    musicbrainz_timeout_seconds: float = Field(default=10.0, gt=0)
    musicbrainz_rate_limit_per_second: float = Field(default=1.0, gt=0)

    @field_validator("music_source_roots", mode="before")
    @classmethod
    def parse_music_source_roots(cls, value: object) -> object:
        """Allow roots to be provided as a comma-separated string."""
        if value is None:
            return []

        if isinstance(value, str):
            cleaned = [item.strip() for item in value.split(",") if item.strip()]
            return cleaned

        if isinstance(value, Path):
            return [value]

        return value

    @field_validator("log_level", mode="before")
    @classmethod
    def normalize_log_level(cls, value: object) -> object:
        """Normalize log level values so env input is case-insensitive."""
        if isinstance(value, str):
            return value.upper()
        return value


@lru_cache(maxsize=1)
def get_settings() -> AppSettings:
    """Load settings once and reuse for process lifetime."""
    return AppSettings()
