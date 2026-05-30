from datetime import datetime

from marionette.application.protocols import CharacterRepository, VoteRepository
from marionette.application.protocols.transaction import Transaction
from marionette.application.protocols.types import CharacterId, UserId
from marionette.domain.exceptions import VoteOnCooldown
from marionette.domain.policies.character_policy import CharacterPolicy
from marionette.domain.policies.vote_policy import VotePolicy
from marionette.domain.services.rating_service import RatingChangeReason, RatingService


class VoteUseCase:
    def __init__(
        self,
        rating_service: RatingService,
        character_repo: CharacterRepository,
        vote_repo: VoteRepository,
        transaction: Transaction,
    ) -> None:
        self._rating_service = rating_service
        self._character_repository = character_repo
        self._vote_repository = vote_repo
        self._transaction = transaction

    # TODO: Если ты подписчик конкретного персонажа,
    #   ты можешь голосовать обычно, либо "нейтрально" - отметиться, что был, но не давать рейтинга. Но ты не можешь голосовать отрицательно.
    #   Если же ты НЕ подписчик, то можно голосовать отрицательно
    async def vote_for(self, voted_by: UserId, user_id: UserId, character_name: str, now: datetime) -> None:
        async with self._transaction:
            character = await self._character_repository.get_by_user_id_and_name(user_id=user_id, name=character_name)
            CharacterPolicy.ensure_character_exists(character, character_name)

            assert character is not None
            VotePolicy.ensure_character_is_applied(character, character_name)

            vote = await self._vote_repository.get_vote_by_character_id(character_id=CharacterId(character.id))
            if vote is not None and VotePolicy.is_on_cooldown(vote=vote, now=now):
                raise VoteOnCooldown(character.name, VotePolicy.cooldown_remaining(vote=vote, now=now))

            d_rating = self._rating_service.inc_character_rating(rating=5, reason=RatingChangeReason.VOTE, in_agency=character.agency_id is not None)
            character.rating += d_rating
            if vote is None:
                self._vote_repository.create(character_id=CharacterId(character.id), vote_time=now, voted_by=voted_by)
            else:
                vote.voted_at = now
                vote.voted_by = voted_by

            await self._transaction.commit()
