from dataclasses import dataclass

import miru
from dishka import AsyncContainer


@dataclass
class CrescentContainer:
    dishka: AsyncContainer
    component_client: miru.Client
