import os
from dataclasses import dataclass, field


@dataclass
class Config:
    # Bot
    MARIONETTE_TOKEN: str = os.environ["MARIONETTE_TOKEN"]

    # Discord
    MAIN_GUILD_ID: int = int(os.environ["MAIN_GUILD_ID"])
    NEWS_CHANNEL_ID: int = int(os.environ["NEWS_CHANNEL_ID"])
    TABLOID_CHANNEL_ID: int = int(os.environ["TABLOID_CHANNEL_ID"])
    PAPARAZZI_TRIGGER_CHANNEL_PREFIX: str = os.environ.get(
        "PAPARAZZI_TRIGGER_CHANNEL_PREFIX", "PP"
    )
    REGISTRATION_CHANNEL_ID: int = int(os.environ["REGISTRATION_CHANNEL_ID"])
    RP_CATEGORIES: list[int] = field(
        default_factory=lambda: [
            int(category_id)
            for category_id in os.environ.get("RP_CATEGORIES", "").split(",")
            if category_id.strip()
        ]
    )
    ONBOARDING_WELCOME_CHANNEL_ID: int = int(os.environ["ONBOARDING_WELCOME_CHANNEL_ID"])
    ONBOARDING_INTRO_CHANNEL_ID: int = int(os.environ["ONBOARDING_INTRO_CHANNEL_ID"])
    ONBOARDING_RULES_CHANNEL_ID: int = int(os.environ["ONBOARDING_RULES_CHANNEL_ID"])
    ONBOARDING_FAQ_CHANNEL_ID: int = int(os.environ["ONBOARDING_FAQ_CHANNEL_ID"])

    # Discord Roles
    UNVERIFIED_ROLE_ID: int = int(os.environ["UNVERIFIED_ROLE_ID"])
    START_ROLE_ID: int = int(os.environ["START_ROLE_ID"])
    UNREGISTERED_ROLE_ID: int = int(os.environ["UNREGISTERED_ROLE_ID"])

    # Infrastructure
    DATABASE_URL: str = os.environ["DATABASE_URL"]
    REDIS_URL: str = os.environ["REDIS_URL"]

    DATABASE_POOL_SIZE: int = int(os.environ.get("DATABASE_POOL_SIZE", "10"))
    DATABASE_MAX_OVERFLOW: int = int(os.environ.get("DATABASE_MAX_OVERFLOW", "20"))


config = Config()
