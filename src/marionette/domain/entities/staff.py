from collections.abc import Sequence
from enum import StrEnum
from typing import Final

from sqlalchemy.orm import Mapped, mapped_column

from marionette.domain.entities.base import Base
from marionette.domain.permissions.approve_character import ApproveCharacterPermission
from marionette.domain.permissions.ignore_entrance import IgnoreEntrancePermission
from marionette.domain.permissions.permission import Permission
from sqlalchemy.types import ARRAY, String


class StaffRoles(StrEnum):
    GAME_MASTER = "gamemaster"
    CHARACTER_CHECKER = "characterchecker"
    ALL_MIGHT = "allmight"

    def has_permission(self, permission: Permission) -> bool:
        return permission in STAFF_ROLE_TO_PERMISSIONS[self]


STAFF_ROLE_TO_PERMISSIONS: Final[dict[str, Sequence[Permission]]] = {
    StaffRoles.GAME_MASTER: [IgnoreEntrancePermission],
    StaffRoles.ALL_MIGHT: [IgnoreEntrancePermission, ApproveCharacterPermission],
    StaffRoles.CHARACTER_CHECKER: [ApproveCharacterPermission],
}


class Staff(Base):
    __tablename__ = "staff"

    id: Mapped[int] = mapped_column(primary_key=True)

    user_id: Mapped[int] = mapped_column()
    """User ID персонала"""

    role: Mapped[StaffRoles] = mapped_column()
    """Роль персонала"""

    permissions: Mapped[list[str]] = mapped_column(ARRAY(String))
    """
    Права в виде `[permissions.<code>, permissions.<code_2>]`. Сделал так, потому что не вижу смысла переусложнять с нормальной системой, лол.
    Тут и так не NF3, так что не страшно, да и записей будет не столь много, как можно подумать
    """
