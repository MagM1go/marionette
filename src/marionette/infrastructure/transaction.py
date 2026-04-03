from types import TracebackType
from typing import Self

from sqlalchemy.ext.asyncio import AsyncSession

from marionette.application.protocols import Transaction


class SqlAlchemyTransaction(Transaction):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def commit(self) -> None:
        await self._session.commit()

    async def rollback(self) -> None:
        await self._session.rollback()

    async def __aenter__(self) -> Self:
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None = None,
        exc: BaseException | None = None,
        exc_traceback: TracebackType | None = None,
    ) -> None:
        if exc_type is not None:
            await self.rollback()
