from dataclasses import dataclass


@dataclass
class PaparazziExposeData:
    exposed_character_name: str
    expose_channel_id: int
