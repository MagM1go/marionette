from dataclasses import dataclass

from dishka import AsyncContainer


@dataclass
class CrescentContainer:
    dishka: AsyncContainer
