import typing as t

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from marionette.domain.uow import IUnitOfWork
from marionette.infrastructure.repositories.agency_repository import AgencyRepository
from marionette.infrastructure.repositories.character_repository import CharacterRepository


class UnitOfWork(IUnitOfWork):
    def __init__(self, factory: async_sessionmaker[AsyncSession]) -> None:
        self._session_factory: async_sessionmaker[AsyncSession] = factory

    @t.override
    async def __aenter__(self) -> "IUnitOfWork":
        self._session = self._session_factory()
        self.agency_repo = AgencyRepository(self._session)
        self.character_repo = CharacterRepository(self._session)
        return self

    @t.override
    async def __aexit__(self, exc_type: Exception, *args: list[str]) -> None:
        if exc_type:
            await self._session.rollback()

        await self._session.close()

    @t.override
    async def commit(self) -> None:
        await self._session.commit()

    @t.override
    async def rollback(self) -> None:
        await self._session.rollback()
