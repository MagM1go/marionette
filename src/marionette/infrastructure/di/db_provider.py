from collections.abc import AsyncGenerator

from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import AsyncSession

from marionette.application.usecases.entrance_usecase import EntranceUseCase
from marionette.application.usecases.exit_usecase import ExitUseCase
from marionette.application.usecases.paparazzi_usecase import PaparazziUseCase
from marionette.domain.repositories import (
    IAgencyRepository,
    ICharacterRepository,
    ICooldownRepository,
)
from marionette.domain.services.rating_service import RatingService
from marionette.domain.services.roleplay_service import RoleplayService
from marionette.domain.uow import IUnitOfWork
from marionette.infrastructure.cache.redis import RedisManager
from marionette.infrastructure.config import config
from marionette.infrastructure.db.manager import DBManager
from marionette.infrastructure.repositories.agency_repository import AgencyRepository
from marionette.infrastructure.repositories.character_repository import (
    CharacterRepository,
)
from marionette.infrastructure.repositories.redis_repository import CooldownRepository
from marionette.infrastructure.repositories.uow import UnitOfWork


class ApplicationProvider(Provider):
    @provide(scope=Scope.APP)
    async def db_manager(self) -> AsyncGenerator[DBManager, None]:
        manager = DBManager(config.DATABASE_URL)
        yield manager
        await manager.dispose()

    @provide(scope=Scope.REQUEST)
    async def session(self, manager: DBManager) -> AsyncGenerator[AsyncSession, None]:
        async with manager.get_session() as session:
            yield session

    @provide(scope=Scope.APP)
    async def redis_manager(self) -> AsyncGenerator[RedisManager, None]:
        manager = RedisManager(config.REDIS_URL)
        yield manager
        await manager.dispose()

    @provide(scope=Scope.REQUEST)
    def cooldown_repository(self, manager: RedisManager) -> ICooldownRepository:
        return CooldownRepository(manager.client)

    @provide(scope=Scope.REQUEST)
    def character_repository(self, session: AsyncSession) -> ICharacterRepository:
        return CharacterRepository(session)

    @provide(scope=Scope.REQUEST)
    def agency_repository(self, session: AsyncSession) -> IAgencyRepository:
        return AgencyRepository(session)

    @provide(scope=Scope.REQUEST)
    def uow(self, manager: DBManager) -> IUnitOfWork:
        return UnitOfWork(manager.session_factory)

    @provide(scope=Scope.REQUEST)
    def rating_service(
        self,
        character_repo: ICharacterRepository,
        agency_repo: IAgencyRepository,
        uow: IUnitOfWork,
    ) -> RatingService:
        return RatingService(
            character_repo=character_repo, agency_repo=agency_repo, uow=uow
        )

    @provide(scope=Scope.REQUEST)
    def roleplay_service(
        self, character_repo: ICharacterRepository, agency_repo: IAgencyRepository
    ) -> RoleplayService:
        return RoleplayService(character_repo=character_repo, agency_repo=agency_repo)

    @provide(scope=Scope.REQUEST)
    def expose_usecase(
        self,
        rating_service: RatingService,
        uow: IUnitOfWork,
        cooldown_repo: ICooldownRepository,
    ) -> PaparazziUseCase:
        return PaparazziUseCase(
            rating_service=rating_service,
            uow=uow,
            cooldown_repo=cooldown_repo,
        )

    @provide(scope=Scope.REQUEST)
    def entrance_usecase(self, roleplay_service: RoleplayService) -> EntranceUseCase:
        return EntranceUseCase(roleplay_service=roleplay_service)

    @provide(scope=Scope.REQUEST)
    def exit_usecase(self, roleplay_service: RoleplayService) -> ExitUseCase:
        return ExitUseCase(roleplay_service=roleplay_service)
