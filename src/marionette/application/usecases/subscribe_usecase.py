from marionette.application.protocols import SubscriptionRepository, Transaction
from marionette.application.protocols.types import CharacterId, UserId
from marionette.domain.exceptions import AlreadySubscribed, CanNotSubscribeYourself


class SubscribeUseCase:
    def __init__(self, repository: SubscriptionRepository, transaction: Transaction) -> None:
        self._repository = repository
        self._transaction = transaction

    async def subscribe(self, subscriber_id: UserId, character_author_id: UserId, character_id: CharacterId) -> None:
        if subscriber_id == character_author_id:
            raise CanNotSubscribeYourself()

        async with self._transaction:
            subscriptions = await self._repository.get_follower_subscriptions(subscriber_id)

            if subscriptions is not None:
                for sub in subscriptions:
                    if sub.character_id == character_id:
                        raise AlreadySubscribed()

            self._repository.subscribe(user_id=subscriber_id, character_author_id=character_author_id, character_id=character_id)
            await self._transaction.commit()
