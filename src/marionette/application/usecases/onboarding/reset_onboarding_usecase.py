from datetime import UTC, datetime

from marionette.application.protocols.onboarding_repository import OnboardingRepository
from marionette.application.protocols.transaction import Transaction
from marionette.application.protocols.types import UserId


class OnboardingResetUseCase:
    def __init__(self, transaction: Transaction, repository: OnboardingRepository) -> None:
        self._transaction = transaction
        self._repository = repository

    async def reset(self, user_id: UserId) -> None:
        async with self._transaction:
            await self._repository.reset(user_id, updated_at=datetime.now(UTC))
            await self._transaction.commit()
