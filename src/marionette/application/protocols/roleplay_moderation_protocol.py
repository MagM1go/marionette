from typing import Protocol


class RoleplayModeration(Protocol):
    def is_rp_location(self, location: object) -> bool: ...
