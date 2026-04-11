from datetime import datetime

from sqlalchemy import select, update
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from marionette.application.protocols import OnboardingRepository
from marionette.application.protocols.types import UserId
from marionette.domain.entities.onboarding import (
    OnboardingEvent,
    OnboardingState,
    OnboardingStep,
)


class SqlAlchemyOnboardingRepository(OnboardingRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create(self, user_id: UserId, created_at: datetime) -> OnboardingState:
        stmt = (
            insert(OnboardingState)
            .values(
                user_id=user_id,
                current_step=OnboardingStep.NEWBIE,
                is_complete=False,
                created_at=created_at,
            )
            .on_conflict_do_nothing(index_elements=[OnboardingState.user_id])
        )
        await self._session.execute(stmt)

        state = await self.get_by_user_id(user_id)
        if state is None:
            raise RuntimeError(f"failed to create onboarding state for user_id={user_id}")
        return state

    async def get_by_user_id(self, user_id: UserId) -> OnboardingState | None:
        stmt = select(OnboardingState).where(OnboardingState.user_id == user_id)
        result = await self._session.execute(stmt)
        return result.scalar_one_or_none()

    async def reset(self, user_id: UserId, updated_at: datetime) -> OnboardingState:
        stmt = (
            update(OnboardingState)
            .where(OnboardingState.user_id == user_id)
            .values(
                current_step=OnboardingStep.NEWBIE,
                is_complete=False,
                completed_at=None,
                updated_at=updated_at,
            )
            .returning(OnboardingState)
        )
        result = await self._session.execute(stmt)
        return result.scalar_one()

    async def log_event(self, event: OnboardingEvent) -> None:
        self._session.add(event)
