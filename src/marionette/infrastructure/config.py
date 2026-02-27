import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()


@dataclass
class Config:
    MARIONETTE_TOKEN: str = os.environ["MARIONETTE_TOKEN"]

    MAIN_GUILD_ID: int = 1473362979927101635
    TABLOID_CHANNEL_ID: int = 1473711815073726639 

    DATABASE_URL: str = os.environ["DATABASE_URL"]
    REDIS_URL: str = os.environ["REDIS_URL"]


config = Config()
