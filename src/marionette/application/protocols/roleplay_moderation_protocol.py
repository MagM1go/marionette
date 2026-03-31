from typing import Any, Protocol

from marionette.application.protocols.types import LocationId


class RoleplayModeration(Protocol):
    # TODO: я устал почищу Any попозже
    def is_rp_location(self, location_id: LocationId, cache: Any) -> bool: ...
