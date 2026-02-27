import typing as t
from collections.abc import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from marionette.domain.entities.agency import Agency
from marionette.domain.repositories import IAgencyRepository


class AgencyRepository(IAgencyRepository):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    @t.override
    async def save(
        self,
        owner_id: int,
        name: str,
    ) -> Agency | None:
        agency = Agency(owner_id=owner_id, name=name)
        await self.session.flush()
        return agency

    @t.override
    async def update(self) -> None:
        await self.session.flush()

    @t.override
    async def get_all(self) -> Sequence[Agency]:
        result = await self.session.execute(select(Agency))
        return result.scalars().all()

    @t.override
    async def get_agency_by_id(self, id: int) -> Agency | None:
        stmt = select(Agency).where(Agency.id == id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()
