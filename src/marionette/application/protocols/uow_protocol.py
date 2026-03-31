from types import TracebackType
from typing import Protocol, Self


class UnitOfWork(Protocol):
    async def commit(self) -> None: ...
    async def rollback(self) -> None: ...

    async def __aenter__(self) -> Self: ...
    async def __aexit__(
        self,
        exc_type: type[BaseException] | None = None,
        exc: BaseException | None = None,
        exc_traceback: TracebackType | None = None,
    ) -> None: ...
