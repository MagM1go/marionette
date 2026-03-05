import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()


@dataclass
class Config:
    # Bot
    MARIONETTE_TOKEN: str = os.environ["MARIONETTE_TOKEN"]

    # Discord
    MAIN_GUILD_ID: int = int(os.environ["MAIN_GUILD_ID"])
    TABLOID_CHANNEL_ID: int = int(os.environ["TABLOID_CHANNEL_ID"])
    REGISTRATION_CHANNEL_ID: int = int(os.environ["REGISTRATION_CHANNEL_ID"])
    RP_CATEGORIES: list[int] = [
        int(category_id) for category_id in os.environ["RP_CATEGORIES"].split(",")
    ]

    # Infrastructure
    DATABASE_URL: str = os.environ["DATABASE_URL"]
    REDIS_URL: str = os.environ["REDIS_URL"]


config = Config()
