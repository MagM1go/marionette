import datetime
from typing import Protocol

from marionette.application.protocols.types import UserId
from marionette.domain.entities.onboarding import OnboardingEvent, OnboardingState


class OnboardingRepository(Protocol):
    """Хранилище состояния и событий онбординга."""

    async def create(self, user_id: UserId, created_at: datetime.datetime) -> OnboardingState:
        """Создаёт состояние онбординга для пользователя.

        Args:
            user_id: Discord ID пользователя.
            created_at: Время создания состояния.
        """
        ...

    async def get_by_user_id(self, user_id: UserId) -> OnboardingState | None:
        """Возвращает состояние онбординга пользователя.

        Args:
            user_id: Discord ID пользователя.

        Returns:
            Состояние онбординга или None, если пользователь его ещё не начинал.
        """
        ...

    async def reset(self, user_id: UserId, updated_at: datetime.datetime) -> OnboardingState:
        """Сбрасывает состояние онбординга пользователя к начальному шагу.

        Args:
            user_id: Discord ID пользователя.
            updated_at: Время сброса состояния.
        """
        ...

    async def log_event(self, event: OnboardingEvent) -> None:
        """Записывает событие онбординга.

        Args:
            event: Событие онбординга.
        """
        ...
