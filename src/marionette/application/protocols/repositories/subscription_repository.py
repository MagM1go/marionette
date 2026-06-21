import typing as t
from collections.abc import Sequence

from marionette.application.protocols.types import CharacterId, UserId
from marionette.domain.entities.subscription import Subscription


class SubscriptionRepository(t.Protocol):
    def subscribe(self, user_id: UserId, character_author_id: UserId, character_id: CharacterId) -> Subscription: ...

    async def get_follower_subscriptions(self, user_id: UserId) -> Sequence[Subscription] | None: ...

    async def get_follower_subscription_by_character(self, user_id: UserId, character_id: CharacterId) -> Subscription | None: ...
