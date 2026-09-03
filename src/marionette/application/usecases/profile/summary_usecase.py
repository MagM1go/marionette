from collections import Counter
from collections.abc import Sequence
from dataclasses import dataclass
from typing import TYPE_CHECKING

from marionette.application.protocols.repositories.character_repository import CharacterRepository
from marionette.application.protocols.repositories.subscription_repository import SubscriptionRepository
from marionette.application.protocols.transaction import Transaction
from marionette.application.protocols.types import UserId
from marionette.domain.roles import Roles

if TYPE_CHECKING:
    from marionette.domain.entities.character import Character
    from marionette.domain.entities.subscription import Subscription


@dataclass(slots=True, frozen=True)
class SummaryData:
    characters: Sequence[Character]
    subscriptions: Sequence[Subscription]
    most_chosen_role: Roles | None
    average_age: float | None


# достижения;
class ProfileSummaryUseCase:
    def __init__(self, transaction: Transaction, character_repo: CharacterRepository, subscription_repo: SubscriptionRepository) -> None:
        self._transaction = transaction
        self._character_repository = character_repo
        self._subscription_repository = subscription_repo

    def _average_age(self, ages: list[float]) -> float:
        return sum(ages) / len(ages)

    async def summary(self, user_id: UserId) -> SummaryData:
        async with self._transaction:
            characters = await self._character_repository.get_all_characters_by_user_id(user_id=user_id)
            subscriptions = await self._subscription_repository.get_follower_subscriptions(user_id=user_id)

            if not characters:
                return SummaryData(characters=[], subscriptions=subscriptions or [], most_chosen_role=None, average_age=None)

            average_age = self._average_age([c.age for c in characters])
            most_chosen_role = Counter([c.role for c in characters]).most_common(n=1)[0][0]

            return SummaryData(characters=characters, subscriptions=subscriptions or [], most_chosen_role=most_chosen_role, average_age=average_age)
