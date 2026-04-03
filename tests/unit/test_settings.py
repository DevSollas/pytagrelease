from pathlib import Path

import pytest
from pydantic import ValidationError

from src.config.settings import AppSettings


def test_settings_defaults_without_env_file(monkeypatch: pytest.MonkeyPatch) -> None:
    for key in (
        "APP_ENV",
        "APP_HOST",
        "APP_PORT",
        "LOG_LEVEL",
        "MUSIC_SOURCE_ROOTS",
        "MUSIC_SOURCE_ROOT",
        "TAGGED_OUTPUT_ROOT",
        "CLEAR_METADATA",
        "MUSICBRAINZ_USER_AGENT",
        "MUSICBRAINZ_TIMEOUT_SECONDS",
        "MUSICBRAINZ_RATE_LIMIT_PER_SECOND",
    ):
        monkeypatch.delenv(key, raising=False)

    settings = AppSettings()

    assert settings.app_env == "development"
    assert settings.app_host == "0.0.0.0"
    assert settings.app_port == 8000
    assert settings.log_level == "INFO"
    assert settings.music_source_roots == []
    assert settings.tagged_output_root == Path("./tagged-output")
    assert settings.clear_metadata is False
    assert settings.musicbrainz_timeout_seconds == 10.0
    assert settings.musicbrainz_rate_limit_per_second == 1.0


def test_music_source_roots_parses_csv_env(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("MUSIC_SOURCE_ROOTS", "/music/a,/music/b")

    settings = AppSettings()

    assert settings.music_source_roots == [Path("/music/a"), Path("/music/b")]


def test_music_source_root_legacy_alias_is_supported(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("MUSIC_SOURCE_ROOT", "/legacy/music")

    settings = AppSettings()

    assert settings.music_source_roots == [Path("/legacy/music")]


def test_log_level_is_case_insensitive(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("LOG_LEVEL", "debug")

    settings = AppSettings()

    assert settings.log_level == "DEBUG"


def test_invalid_port_fails_validation(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("APP_PORT", "70000")

    with pytest.raises(ValidationError):
        AppSettings()
