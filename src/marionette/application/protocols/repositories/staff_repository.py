from collections.abc import Sequence
from typing import Protocol

from marionette.application.protocols import UserId
from marionette.domain.entities.staff import Staff, StaffRoles
from marionette.domain.permissions.permission import Permission


class StaffRepository(Protocol):
    def create(self, user_id: UserId, role: StaffRoles, permissions: Sequence[Permission]) -> Staff | None:
        """Создаёт запись о новом \"сотруднике\""""
        ...

    async def get_by_user_id(self, user_id: UserId) -> Staff | None: ...
