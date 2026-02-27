from abc import ABC, abstractmethod

from marionette.domain.repositories import IAgencyRepository, ICharacterRepository


class IUnitOfWork(ABC):
    character_repo: ICharacterRepository
    agency_repo: IAgencyRepository

    @abstractmethod
    async def __aenter__(self) -> "IUnitOfWork": ...

    @abstractmethod
    async def __aexit__(self, exc_type: Exception, *args: list[str]) -> None: ...
    
    @abstractmethod
    async def commit(self) -> None: ...

    @abstractmethod
    async def rollback(self) -> None: ...
