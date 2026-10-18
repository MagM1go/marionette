import importlib
import sys
from pathlib import Path
from typing import Any

import pytest
from dature.errors import DatureConfigError

CONFIG_MODULE = "marionette.bootstrap.config"

IDS_YAML = """\
guild:
   main: 42

category:
   roleplay:
      - 1
      - 2
      - 3

text_channels:
   tabloid: 44
   news: 43
   registration: 45

   onboarding:
     welcome: 46
     intro: 47
     rules: 48
     faq: 49

   general: 58
   moderation: 54

forum_channels:
   character: 57

roles:
   unverified: 50
   unregistered: 52
   start: 51
   text: 53
   amplua: 56
   moderator: 55
"""

INFRASTRUCTURE_YAML = """\
database:
   pool_size: 11
   max_overflow: 22
"""


def _reload_config_module() -> Any:
    sys.modules.pop(CONFIG_MODULE, None)
    return importlib.import_module(CONFIG_MODULE)


def _write_config_dir(tmp_path: Path) -> Path:
    config_dir = tmp_path / "config"
    (config_dir / "discord").mkdir(parents=True)
    (config_dir / "discord" / "ids.yaml").write_text(IDS_YAML)
    (config_dir / "infrastructure.yaml").write_text(INFRASTRUCTURE_YAML)
    return config_dir


def _set_required_env(monkeypatch: pytest.MonkeyPatch, **overrides: str) -> None:
    values = {
        "MARIONETTE_TOKEN": "token",
        "DATABASE_URL": "postgresql+psycopg://env:pass@localhost:5432/app",
        "REDIS_URL": "redis://localhost:6379/0",
    }
    values.update(overrides)

    for key in values:
        monkeypatch.setenv(key, values[key])


def test_load_config_maps_yaml_sections_and_env_secrets(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    _set_required_env(monkeypatch)
    config_dir = _write_config_dir(tmp_path)
    config_module = _reload_config_module()

    config = config_module.load_config(env_file=tmp_path / "MISSING.env", config_dir=config_dir)

    assert config.discord.bot_token == "token"
    assert config.discord.guild.main == 42
    assert config.discord.category.roleplay == [1, 2, 3]
    assert config.discord.text_channels.tabloid == 44
    assert config.discord.text_channels.news == 43
    assert config.discord.text_channels.registration == 45
    assert config.discord.text_channels.moderation == 54
    assert config.discord.text_channels.onboarding.welcome == 46
    assert config.discord.text_channels.onboarding.intro == 47
    assert config.discord.text_channels.onboarding.rules == 48
    assert config.discord.text_channels.onboarding.faq == 49
    assert config.discord.text_channels.general == 58
    assert config.discord.forum_channels.character == 57
    assert config.discord.roles.unverified == 50
    assert config.discord.roles.unregistered == 52
    assert config.discord.roles.start == 51
    assert config.discord.roles.text == 53
    assert config.discord.roles.amplua == 56
    assert config.discord.roles.moderator == 55
    assert config.discord.paparazzi_trigger_channel_prefix == "PP"

    assert config.database.url == "postgresql+psycopg://env:pass@localhost:5432/app"
    assert config.database.redis_url == "redis://localhost:6379/0"
    assert config.database.pool_size == 11
    assert config.database.max_overflow == 22


def test_load_config_prefers_environment_over_dotenv(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    env_file = tmp_path / ".env"
    env_file.write_text(
        "\n".join(
            [
                "MARIONETTE_TOKEN=file-token",
                "DATABASE_URL=postgresql+psycopg://file:pass@localhost:5432/app",
                "REDIS_URL=redis://file:6379/0",
                "PAPARAZZI_TRIGGER_CHANNEL_PREFIX=FILEPP",
            ]
        )
    )
    config_dir = _write_config_dir(tmp_path)

    _set_required_env(
        monkeypatch,
        MARIONETTE_TOKEN="env-token",
        DATABASE_URL="postgresql+psycopg://env:pass@localhost:5432/app",
    )
    config_module = _reload_config_module()

    monkeypatch.delenv("REDIS_URL", raising=False)
    monkeypatch.delenv("PAPARAZZI_TRIGGER_CHANNEL_PREFIX", raising=False)

    config = config_module.load_config(env_file=env_file, config_dir=config_dir)

    assert config.discord.bot_token == "env-token"
    assert config.database.url == "postgresql+psycopg://env:pass@localhost:5432/app"
    assert config.database.redis_url == "redis://file:6379/0"
    assert config.discord.paparazzi_trigger_channel_prefix == "FILEPP"
    assert config.discord.guild.main == 42
    assert config.database.pool_size == 11


def test_load_config_fails_when_yaml_and_env_are_missing(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    _set_required_env(monkeypatch)
    config_module = _reload_config_module()

    empty_config_dir = tmp_path / "empty-config"
    empty_config_dir.mkdir()

    with pytest.raises(DatureConfigError):
        config_module.load_config(env_file=tmp_path / "MISSING.env", config_dir=empty_config_dir)
