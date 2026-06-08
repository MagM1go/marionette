from dataclasses import dataclass, field

from dature import F, EnvFileSource, EnvSource, load
from dature.types import FieldMapping


@dataclass
class DiscordConfig:
    bot_token: str

    main_guild_id: int
    news_channel_id: int
    tabloid_channel_id: int
    registration_channel_id: int

    onboarding_welcome_channel_id: int
    onboarding_intro_channel_id: int
    onboarding_rules_channel_id: int
    onboarding_faq_channel_id: int
    
    moderation_channel_id: int

    unverified_role_id: int
    start_role_id: int
    unregistered_role_id: int
    text_role_id: int
    
    moderator_role_id: int
    amplua_role_id: int
    
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
    filename: str = ".env"
) -> T:
    return load(
        EnvFileSource(
            file=filename,
            field_mapping=field_mapping,
            skip_if_broken=True,
        ),
        EnvSource(field_mapping=field_mapping),
        schema=dataclass_,
    )


def load_config(filename: str = ".env") -> Config:
    database_config = _load_section(
        DatabaseConfig,
        field_mapping={
            F[DatabaseConfig].url: "database_url",
            F[DatabaseConfig].pool_size: "database_pool_size",
            F[DatabaseConfig].max_overflow: "database_max_overflow",
        },
        filename=filename
    )
    discord_config = _load_section(
        DiscordConfig,
        field_mapping={
            F[DiscordConfig].bot_token: "marionette_token",
            F[DiscordConfig].main_guild_id: "main_guild_id",
        },
        filename=filename
    )
    return Config(database=database_config, discord=discord_config)


config = load_config()
