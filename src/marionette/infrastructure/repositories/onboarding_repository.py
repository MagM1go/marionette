import typing as t
from datetime import datetime

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from marionette.application.protocols import (
    IOnboardingRepository,
    RoleId,
    UserId,
)
from marionette.domain.entities.onboarding import (
    OnboardingEvent,
    OnboardingRoleGrant,
    OnboardingState,
    OnboardingStep,
)


class OnboardingRepository(IOnboardingRepository):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    @t.override
    def start(self, user_id: UserId) -> None:
        state = OnboardingState(
            user_id=int(user_id),
            current_step=OnboardingStep.WELCOME,
            is_complete=False,
        )
        self.session.add(state)

    async def _get_state(self, user_id: UserId) -> OnboardingState | None:
        stmt = select(OnboardingState).where(OnboardingState.user_id == int(user_id))
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def _get_or_create_state(self, user_id: UserId) -> OnboardingState:
        state = await self._get_state(user_id)
        if state is None:
            self.start(user_id)
            state = await self._get_state(user_id)

        if state is None:
            raise RuntimeError("Failed to initialize onboarding state.")

        return state

    @t.override
    async def get_current_step(self, user_id: UserId) -> OnboardingStep | None:
        state = await self._get_state(user_id)
        return state.current_step if state else None

    @t.override
    async def set_current_step(self, user_id: UserId, step: OnboardingStep) -> None:
        state = await self._get_or_create_state(user_id)
        state.current_step = step

    @t.override
    async def is_complete(self, user_id: UserId) -> bool:
        state = await self._get_state(user_id)
        return bool(state and state.is_complete)

    @t.override
    async def set_complete(self, user_id: UserId) -> None:
        state = await self._get_or_create_state(user_id)
        now = datetime.now()
        state.current_step = OnboardingStep.COMPLETED
        state.is_complete = True
        state.completed_at = now

    @t.override
    async def add_role(self, user_id: UserId, role_id: RoleId) -> None:
        stmt = select(OnboardingRoleGrant).where(
            OnboardingRoleGrant.user_id == int(user_id),
            OnboardingRoleGrant.role_id == int(role_id),
        )
        result = await self.session.execute(stmt)
        existing = result.scalar_one_or_none()
        if existing is not None:
            return

        self.session.add(
            OnboardingRoleGrant(
                user_id=int(user_id),
                role_id=int(role_id),
            )
        )

    @t.override
    async def remove_role(self, user_id: UserId, role_id: RoleId) -> None:
        await self.session.execute(
            delete(OnboardingRoleGrant).where(
                OnboardingRoleGrant.user_id == int(user_id),
                OnboardingRoleGrant.role_id == int(role_id),
            )
        )

    @t.override
    async def get_roles(self, user_id: UserId) -> list[RoleId]:
        stmt = select(OnboardingRoleGrant.role_id).where(
            OnboardingRoleGrant.user_id == int(user_id)
        )
        result = await self.session.execute(stmt)
        return [RoleId(role_id) for role_id in result.scalars().all()]

    @t.override
    async def reset(self, user_id: UserId) -> None:
        await self.session.execute(
            delete(OnboardingRoleGrant).where(OnboardingRoleGrant.user_id == int(user_id))
        )
        await self.session.execute(
            delete(OnboardingState).where(OnboardingState.user_id == int(user_id))
        )

    @t.override
    async def log_event(
        self,
        user_id: UserId,
        event_name: str,
        step: OnboardingStep | None = None,
        metadata: dict[str, str] | None = None,
        created_at: datetime | None = None,
    ) -> None:
        self.session.add(
            OnboardingEvent(
                user_id=int(user_id),
                event_name=event_name,
                step=step,
                payload=metadata or {},
                created_at=created_at or datetime.now(),
            )
        )
