import typing as t
from collections.abc import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from marionette.application.protocols import AgencyRepository
from marionette.domain.entities.agency import Agency


class SqlAlchemyAgencyRepository(AgencyRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    @t.override
    def create(self, owner_id: int, name: str) -> Agency | None:
        agency = Agency(owner_id=owner_id, name=name)
        self._session.add(agency)
        return agency

    @t.override
    async def get_all(self) -> Sequence[Agency]:
        result = await self._session.scalars(select(Agency))
        return result.all()

    @t.override
    async def get_agency_by_id(self, id: int) -> Agency | None:
        stmt = select(Agency).where(Agency.id == id)
        return await self._session.scalar(stmt)
