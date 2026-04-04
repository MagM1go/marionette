from typing import Protocol

from marionette.application.protocols.types import LocationId


class RoleplayModeration(Protocol):
    async def is_rp_location(self, location_id: LocationId) -> bool: ...
