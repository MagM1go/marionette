from datetime import datetime

from marionette.application.protocols import CharacterId, UserId
from marionette.application.protocols.repositories import CharacterRepository
from marionette.application.protocols.repositories.vote_repository import VoteRepository
from marionette.application.protocols.transaction import Transaction
from marionette.domain.entities.vote import VoteSource
from marionette.domain.exceptions import AlreadyVotedForPerfomance, CanNotVoteYourself
from marionette.domain.policies.character_policy import CharacterPolicy


class PerfomanceVoteUseCase:
    def __init__(self, transaction: Transaction, vote_repository: VoteRepository, character_repository: CharacterRepository) -> None:
        self._vote_repository = vote_repository
        self._character_repository = character_repository
        self._transaction = transaction

    async def vote(self, character_id: CharacterId, voted_by: UserId, now: datetime, reputation: int, perfomance_id: int) -> None:
        async with self._transaction:
            character = await self._character_repository.get_by_character_id(character_id=character_id)
            CharacterPolicy.ensure_character_exists(character=character, expected_name=str(character_id))

            assert character is not None
            if character.user_id == voted_by:
                raise CanNotVoteYourself()

            existing_vote = await self._vote_repository.get_vote_by_voter_and_perfomance_id(voted_by=voted_by, perfomance_id=perfomance_id)
            if existing_vote is not None:
                raise AlreadyVotedForPerfomance()

            self._vote_repository.create(
                character_id=character_id,
                vote_time=now,
                voted_by=voted_by,
                reputation=reputation,
                source=VoteSource.REVIEW,
                perfomance_id=perfomance_id,
            )

            await self._transaction.commit()
