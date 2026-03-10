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
    REGISTRATION_CHANNEL_ID: int = int(os.environ["REGISTRATION_CHANNEL_ID"])
    RP_CATEGORIES: list[int] = field(
        default_factory=lambda: [
            int(category_id) for category_id in os.environ["RP_CATEGORIES"].split(",")
        ]
    )

    # Infrastructure
    DATABASE_URL: str = os.environ["DATABASE_URL"]
    REDIS_URL: str = os.environ["REDIS_URL"]


config = Config()
