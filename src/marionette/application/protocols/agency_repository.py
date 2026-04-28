from collections.abc import Sequence
from typing import Protocol

from marionette.application.protocols.types import AgencyId, UserId
from marionette.domain.entities.agency import Agency


class AgencyRepository(Protocol):
    def create(
        self,
        owner_id: UserId,
        name: str,
    ) -> Agency | None:
        """Создаёт новое агентство.

        Args:
            owner_id: Discord ID владельца (директора) агентства.
            name: Название агентства.

        Returns:
            Созданное агентство или None, если агентство с таким именем уже существует.
        """

    async def get_all(self) -> Sequence[Agency]:
        """Возвращает все агентства."""
        ...

    async def get_agency_by_id(self, agency_id: AgencyId) -> Agency | None:
        """Возвращает агентство по его ID.

        Args:
            agency_id: ID агентства в базе данных.

        Returns:
            Агентство или None,
        """
