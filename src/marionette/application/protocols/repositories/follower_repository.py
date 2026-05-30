import typing as t
from collections.abc import Sequence

from marionette.application.protocols.types import UserId
from marionette.domain.entities.follower import Follower
from marionette.domain.entities.subscription import Subscription


class FollowerRepository(t.Protocol):
    def create(self, user_id: UserId) -> Follower: ...

    def get_follower_subscriptions(self, user_id: UserId) -> Sequence[Subscription]: ...

    def get_subscriptions_by_author(self, subscription_user_id: UserId) -> Sequence[Subscription]: ...
