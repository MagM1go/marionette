from collections.abc import AsyncGenerator

from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.ext.asyncio.engine import AsyncEngine

from marionette.application.protocols import UnitOfWork
from marionette.bootstrap.config import config
from marionette.infrastructure.uow import SqlAlchemyUnitOfWork


class DatabaseProvider(Provider):
    scope = Scope.REQUEST

    @provide(scope=Scope.APP)
    async def engine(self) -> AsyncGenerator[AsyncEngine]:
        engine = create_async_engine(
            url=config.database.url,
            pool_pre_ping=True,
            pool_size=config.database.pool_size,
            max_overflow=config.database.max_overflow,
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

    @provide
    async def session(
        self, factory: async_sessionmaker[AsyncSession]
    ) -> AsyncGenerator[AsyncSession]:
        async with factory() as session:
            yield session

    uow = provide(SqlAlchemyUnitOfWork, provides=UnitOfWork)
