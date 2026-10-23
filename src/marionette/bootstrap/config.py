from dataclasses import dataclass
from pathlib import Path

from dature import EnvFileSource, EnvSource, F, Yaml12Source, load
from dature.type_aliases import FieldMapping


@dataclass(frozen=True)
class GuildIds:
    main: int


@dataclass(frozen=True)
class CategoryIds:
    roleplay: list[int]


@dataclass(frozen=True)
class OnboardingChannelIds:
    welcome: int
    intro: int
    rules: int
    faq: int


@dataclass(frozen=True)
class TextChannelIds:
    tabloid: int
    news: int
    registration: int
    moderation: int
    onboarding: OnboardingChannelIds
    general: int


@dataclass(frozen=True)
class ForumChannelIds:
    character: int


@dataclass(frozen=True)
class RoleIds:
    unverified: int
    unregistered: int
    start: int
    text: int
    amplua: int
    moderator: int

    agency_director: int
    agency_manager: int
    idol: int
    actor: int
    singer: int
    mangaka: int
    writer: int
    agent: int
    lawyer: int
    medicine: int
    stylist: int


@dataclass(frozen=True)
class DiscordConfig:
    bot_token: str

    guild: GuildIds
    category: CategoryIds
    text_channels: TextChannelIds
    forum_channels: ForumChannelIds
    roles: RoleIds

    paparazzi_trigger_channel_prefix: str = "PP"


@dataclass(frozen=True)
class DatabaseConfig:
    url: str
    redis_url: str
    pool_size: int = 10
    max_overflow: int = 20


@dataclass(frozen=True)
class Config:
    discord: DiscordConfig
    database: DatabaseConfig


_ENV_DATABASE: FieldMapping = {
    F[DatabaseConfig].url: "DATABASE_URL",
    F[DatabaseConfig].redis_url: "REDIS_URL",
}

_ENV_DISCORD: FieldMapping = {
    F[DiscordConfig].bot_token: "MARIONETTE_TOKEN",
    F[DiscordConfig].paparazzi_trigger_channel_prefix: "PAPARAZZI_TRIGGER_CHANNEL_PREFIX",
}


def load_config(env_file: str | Path = ".env", config_dir: str | Path = "config") -> Config:
    config_path = Path(config_dir)

    database = load(
        Yaml12Source(file=config_path / "infrastructure.yaml", prefix="database", skip_if_missing=True),
        EnvFileSource(file=env_file, field_mapping=_ENV_DATABASE, skip_if_missing=True),
        EnvSource(field_mapping=_ENV_DATABASE),
        schema=DatabaseConfig,
    )
    discord = load(
        Yaml12Source(file=config_path / "discord" / "ids.yaml", skip_if_missing=True),
        EnvFileSource(file=env_file, field_mapping=_ENV_DISCORD, skip_if_missing=True),
        EnvSource(field_mapping=_ENV_DISCORD),
        schema=DiscordConfig,
    )
    return Config(discord=discord, database=database)


config = load_config()
