from collections.abc import Sequence
from datetime import UTC, datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio.session import AsyncSession

from marionette.application.protocols.repositories.subscription_repository import SubscriptionRepository
from marionette.application.protocols.types import CharacterId, UserId
from marionette.domain.entities.subscription import Subscription


class SqlAlchemySubscriptionRepository(SubscriptionRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    def subscribe(self, user_id: UserId, character_author_id: UserId, character_id: CharacterId) -> Subscription:
        subscription = Subscription(follower_id=user_id, character_author_id=character_author_id, character_id=character_id, followed_at=datetime.now(UTC))
        self._session.add(subscription)
        return subscription

    async def get_follower_subscriptions(self, user_id: UserId) -> Sequence[Subscription] | None:
        stmt = select(Subscription).where(Subscription.follower_id == user_id)
        result = await self._session.scalars(stmt)
        return result.all()

    async def get_follower_subscription_by_character(self, user_id: UserId, character_id: CharacterId) -> Subscription | None:
        stmt = select(Subscription).where(Subscription.follower_id == user_id, Subscription.character_id == character_id)
        return await self._session.scalar(stmt)  # type: ignore[no-any-return]
