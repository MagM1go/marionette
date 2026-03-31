from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm.strategy_options import selectinload

from marionette.application.protocols import OnboardingRepository
from marionette.domain.entities.onboarding import OnboardingEvent, OnboardingState


class SqlAlchemyOnboardingRepository(OnboardingRepository):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_by_user_id(self, user_id: int) -> OnboardingState | None:
        stmt = (
            select(OnboardingState)
            .options(selectinload(OnboardingState.roles))
            .where(OnboardingState.user_id == user_id)
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    def add(self, state: OnboardingState) -> None:
        self.session.add(state)

    async def log_event(self, event: OnboardingEvent) -> None:
        self.session.add(event)
