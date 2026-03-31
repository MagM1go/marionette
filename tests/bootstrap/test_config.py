import importlib
import sys
from pathlib import Path
from typing import Any

import pytest

CONFIG_MODULE = "marionette.bootstrap.config"


def _reload_config_module() -> Any:
    sys.modules.pop(CONFIG_MODULE, None)
    return importlib.import_module(CONFIG_MODULE)


def _set_required_env(monkeypatch: pytest.MonkeyPatch, **overrides: str) -> None:
    values = {
        "MARIONETTE_TOKEN": "token",
        "DATABASE_URL": "postgresql+psycopg://env:pass@localhost:5432/app",
        "REDIS_URL": "redis://localhost:6379/0",
        "MAIN_GUILD_ID": "42",
        "NEWS_CHANNEL_ID": "43",
        "TABLOID_CHANNEL_ID": "44",
        "REGISTRATION_CHANNEL_ID": "45",
        "RP_CATEGORIES": "1, 2,3",
        "ONBOARDING_WELCOME_CHANNEL_ID": "46",
        "ONBOARDING_INTRO_CHANNEL_ID": "47",
        "ONBOARDING_RULES_CHANNEL_ID": "48",
        "ONBOARDING_FAQ_CHANNEL_ID": "49",
        "UNVERIFIED_ROLE_ID": "50",
        "START_ROLE_ID": "51",
        "UNREGISTERED_ROLE_ID": "52",
    }
    values.update(overrides)

    for key in values:
        monkeypatch.setenv(key, values[key])


def test_load_config_reads_environment_without_dotenv_file(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    _set_required_env(monkeypatch, DATABASE_POOL_SIZE="77")
    config_module = _reload_config_module()

    config = config_module.load_config(env_file=tmp_path / ".env.missing")

    assert config.database.url == "postgresql+psycopg://env:pass@localhost:5432/app"
    assert config.database.pool_size == 77
    assert config.database.max_overflow == 20
    assert config.discord.main_guild_channel == 42
    assert config.discord.paparazzi_trigger_channel_prefix == "PP"
    assert config.discord.rp_categories == [1, 2, 3]


def test_load_config_prefers_environment_over_dotenv(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    env_file = tmp_path / ".env"
    env_file.write_text(
        "\n".join(
            [
                "MARIONETTE_TOKEN=file-token",
                "DATABASE_URL=postgresql+psycopg://file:pass@localhost:5432/app",
                "DATABASE_POOL_SIZE=11",
                "DATABASE_MAX_OVERFLOW=22",
                "REDIS_URL=redis://file:6379/0",
                "MAIN_GUILD_ID=100",
                "NEWS_CHANNEL_ID=101",
                "TABLOID_CHANNEL_ID=102",
                "REGISTRATION_CHANNEL_ID=103",
                "PAPARAZZI_TRIGGER_CHANNEL_PREFIX=FILEPP",
                "RP_CATEGORIES=[4,5]",
                "ONBOARDING_WELCOME_CHANNEL_ID=104",
                "ONBOARDING_INTRO_CHANNEL_ID=105",
                "ONBOARDING_RULES_CHANNEL_ID=106",
                "ONBOARDING_FAQ_CHANNEL_ID=107",
                "UNVERIFIED_ROLE_ID=108",
                "START_ROLE_ID=109",
                "UNREGISTERED_ROLE_ID=110",
            ]
        )
    )

    _set_required_env(
        monkeypatch,
        MARIONETTE_TOKEN="env-token",
        DATABASE_URL="postgresql+psycopg://env:pass@localhost:5432/app",
        RP_CATEGORIES="9,10",
        MAIN_GUILD_ID="999",
    )
    config_module = _reload_config_module()

    config = config_module.load_config(env_file=env_file)

    assert config.discord.bot_token == "env-token"
    assert config.database.url == "postgresql+psycopg://env:pass@localhost:5432/app"
    assert config.discord.main_guild_channel == 999
    assert config.discord.rp_categories == [9, 10]
    assert config.database.pool_size == 11
    assert config.database.max_overflow == 22
    assert config.discord.paparazzi_trigger_channel_prefix == "FILEPP"
