from typing import Protocol

from marionette.application.protocols.types import LocationId


class RoleplayModeration(Protocol):
    """Проверяет настройки ролевых локаций."""

    async def is_rp_location(self, location_id: LocationId) -> bool:
        """Возвращает True, если канал является ролевой локацией.

        Args:
            location_id: ID локации.
        """
        ...
