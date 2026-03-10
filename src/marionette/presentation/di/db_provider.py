from collections.abc import AsyncGenerator

from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from marionette.application.protocols import (
    IAgencyRepository,
    ICharacterRepository,
    ICooldownRepository,
)
from marionette.application.usecases.entrance_usecase import EntranceUseCase
from marionette.application.usecases.exit_usecase import ExitUseCase
from marionette.application.usecases.paparazzi_usecase import PaparazziUseCase
from marionette.application.usecases.season_reset_usecase import SeasonResetUseCase
from marionette.domain.services.rating_service import RatingService
from marionette.infrastructure.config import config
from marionette.infrastructure.db.cache.redis import RedisManager
from marionette.infrastructure.repositories.agency_repository import AgencyRepository
from marionette.infrastructure.repositories.character_repository import (
    CharacterRepository,
)
from marionette.infrastructure.repositories.redis_repository import CooldownRepository


class ApplicationProvider(Provider):
    @provide(scope=Scope.APP)
    async def engine(self) -> AsyncGenerator[AsyncEngine, None]:
        engine = create_async_engine(
            url=config.DATABASE_URL,
            echo=False,
            pool_pre_ping=True,
            pool_size=10,
            max_overflow=20,
        )
        yield engine
        await engine.dispose()

    @provide(scope=Scope.APP)
    def session_factory(self, engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
        return async_sessionmaker(
            bind=engine,
            expire_on_commit=False,
            class_=AsyncSession,
        )

    @provide(scope=Scope.REQUEST)
    async def session(
        self, factory: async_sessionmaker[AsyncSession]
    ) -> AsyncGenerator[AsyncSession, None]:
        async with factory() as session:
            try:
                yield session
                await session.commit()
            except Exception:
                await session.rollback()
                raise

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
    def rating_service(self) -> RatingService:
        return RatingService()

    @provide(scope=Scope.REQUEST)
    def expose_usecase(
        self,
        rating_service: RatingService,
        session: AsyncSession,
        cooldown_repo: ICooldownRepository,
    ) -> PaparazziUseCase:
        return PaparazziUseCase(
            rating_service=rating_service,
            session=session,
            cooldown_repo=cooldown_repo,
        )

    @provide(scope=Scope.REQUEST)
    def entrance_usecase(self, character_repo: ICharacterRepository) -> EntranceUseCase:
        return EntranceUseCase(character_repo=character_repo)

    @provide(scope=Scope.REQUEST)
    def exit_usecase(self, character_repo: ICharacterRepository) -> ExitUseCase:
        return ExitUseCase(character_repo=character_repo)

    @provide(scope=Scope.REQUEST)
    def season_reset_usecase(
        self,
        character_repo: ICharacterRepository,
        agency_repo: IAgencyRepository,
    ) -> SeasonResetUseCase:
        return SeasonResetUseCase(
            character_repo=character_repo,
            agency_repo=agency_repo,
        )
