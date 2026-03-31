from dataclasses import dataclass, field
from pathlib import Path

from dature import F, Merge, Source, TypeLoader, load
from dature.types import FieldMapping

_ENV_FILE = Path(__file__).resolve().parents[3] / ".env"


def _parse_int_list(value: object) -> list[int]:
    if value == "" or value is None:
        return []
    if isinstance(value, list):
        return [int(item) for item in value]
    if isinstance(value, str):
        return [int(item.strip()) for item in value.split(",") if item.strip()]
    msg = f"Expected a list or comma-separated string, got {type(value).__name__}"
    raise TypeError(msg)


_TYPE_LOADERS = (TypeLoader(list[int], _parse_int_list),)


@dataclass
class DiscordConfig:
    bot_token: str

    main_guild_channel: int
    news_channel_id: int
    tabloid_channel_id: int
    registration_channel_id: int

    onboarding_welcome_channel_id: int
    onboarding_intro_channel_id: int
    onboarding_rules_channel_id: int
    onboarding_faq_channel_id: int

    unverified_role_id: int
    start_role_id: int
    unregistered_role_id: int
    paparazzi_trigger_channel_prefix: str = "PP"
    rp_categories: list[int] = field(default_factory=list)


@dataclass
class DatabaseConfig:
    url: str
    redis_url: str
    pool_size: int = 10
    max_overflow: int = 20


@dataclass
class Config:
    discord: DiscordConfig
    database: DatabaseConfig


def _load_section[T](
    dataclass_: type[T],
    *,
    field_mapping: FieldMapping | None = None,
    env_file: Path = _ENV_FILE,
) -> T:
    return load(
        Merge(
            Source(
                file_=env_file,
                field_mapping=field_mapping,
                skip_if_broken=True,
            ),
            Source(field_mapping=field_mapping),
            type_loaders=_TYPE_LOADERS,
        ),
        dataclass_,
    )


def load_config(*, env_file: Path = _ENV_FILE) -> Config:
    database_config = _load_section(
        DatabaseConfig,
        field_mapping={
            F[DatabaseConfig].url: "database_url",
            F[DatabaseConfig].pool_size: "database_pool_size",
            F[DatabaseConfig].max_overflow: "database_max_overflow",
        },
        env_file=env_file,
    )
    discord_config = _load_section(
        DiscordConfig,
        field_mapping={
            F[DiscordConfig].bot_token: "marionette_token",
            F[DiscordConfig].main_guild_channel: "main_guild_id",
        },
        env_file=env_file,
    )
    return Config(database=database_config, discord=discord_config)


config = load_config()
