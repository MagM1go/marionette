from marionette.application.protocols import Transaction
from marionette.application.protocols.repositories import CharacterRepository, VoteRepository


class PerfomanceObtainUseCase:
    def __init__(self, transaction: Transaction, character_repository: CharacterRepository, perfomance_vote_repository: VoteRepository) -> None:
        self._transaction = transaction
        self._character_repository = character_repository
        self._vote_repository = perfomance_vote_repository

    async def obtain(self) -> None:
        async with self._transaction:
            pairs = await self._vote_repository.get_not_obtained_perfomance_votes()

            for pair in pairs:
                character, vote = pair

                character.reputation += vote.reputation
                vote.obtained = True

            await self._transaction.commit()
