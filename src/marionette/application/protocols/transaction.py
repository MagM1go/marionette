from types import TracebackType
from typing import Protocol, Self


class Transaction(Protocol):
    """Управляет атомарным изменением состояния хранилища."""

    async def commit(self) -> None:
        """Фиксирует изменения текущей транзакции."""
        ...

    async def rollback(self) -> None:
        """Откатывает изменения текущей транзакции."""
        ...

    async def __aenter__(self) -> Self:
        """Открывает транзакционный контекст."""
        ...

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None = None,
        exc: BaseException | None = None,
        exc_traceback: TracebackType | None = None,
    ) -> None:
        """Закрывает транзакционный контекст."""
        ...
