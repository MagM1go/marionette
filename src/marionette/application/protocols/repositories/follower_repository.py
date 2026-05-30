import typing as t

from marionette.application.protocols.types import UserId
from marionette.domain.entities.follower import Follower
from marionette.domain.entities.subscription import Subscription


class FollowerRepository(t.Protocol):
    def create(self, user_id: UserId) -> Follower: ...

    def get_follower_subscriptions(self, user_id: UserId) -> list[Subscription]: ...

    def get_subscriptions_by_author(self, subscription_user_id: UserId): ...
