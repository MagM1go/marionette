from collections.abc import Sequence
import typing as t

from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy.sql import select

from marionette.application.protocols import UserId
from marionette.application.protocols.repositories.staff_repository import StaffRepository
from marionette.domain.entities.staff import Staff, StaffRoles
from marionette.domain.permissions.permission import Permission


class SqlAlchemyStaffRepository(StaffRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    @t.override
    def create(self, user_id: UserId, role: StaffRoles, permissions: Sequence[Permission]) -> Staff:
        staff = Staff(user_id=user_id, role=role, permissions=[perm.code() for perm in permissions])
        self._session.add(staff)
        return staff

    @t.override
    async def get_by_user_id(self, user_id: UserId) -> Staff | None:
        stmt = select(Staff).where(Staff.user_id == user_id)
        return await self._session.scalar(stmt)  # type: ignore[no-any-return]
