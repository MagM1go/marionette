from marionette.application.protocols import CharacterRepository
from marionette.application.protocols.transaction import Transaction
from marionette.application.protocols.types import UserId
from marionette.domain.policies.vote_policy import VotePolicy
from marionette.domain.services.rating_service import RatingChangeReason, RatingService


class VoteUseCase:
    def __init__(
        self,
        rating_service: RatingService,
        character_repo: CharacterRepository,
        transaction: Transaction,
    ) -> None:
        self._rating_service = rating_service
        self._repository = character_repo
        self._transaction = transaction

    # TODO: Если ты подписчик конкретного персонажа, 
    #   ты можешь голосовать обычно, либо "нейтрально" - отметиться, что был, но не давать рейтинга. Но ты не можешь голосовать отрицательно.
    #   Если же ты НЕ подписчик, то можно голосовать отрицательно
    async def vote_for(self, user_id: UserId, character_name: str) -> None:
        async with self._transaction:
            character = await self._repository.get_by_user_id_and_name(
                user_id=user_id, name=character_name
            )
            VotePolicy.ensure_character_exists(character, character_name)

            assert character is not None
            new_rating = self._rating_service.inc_character_rating(
                rating=5, reason=RatingChangeReason.VOTE, in_agency=character.agency_id is not None
            )
            character.rating += new_rating

            await self._transaction.commit()
