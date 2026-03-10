from dataclasses import dataclass

from dishka import AsyncContainer
import miru


@dataclass
class CrescentContainer:
    dishka: AsyncContainer
    component_client: miru.Client
