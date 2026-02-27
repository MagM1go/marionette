from dataclasses import dataclass


@dataclass
class Embed:
    title: str | None = None
    description: str | None = None
    thumbnail_url: str | None = None
    image_url: str | None = None
    footer: str | None = None
    color: int | None = None
    url: str | None = None
