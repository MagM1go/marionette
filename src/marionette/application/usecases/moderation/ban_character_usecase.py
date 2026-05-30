from marionette.application.protocols import Transaction
from marionette.application.protocols.repositories import CharacterRepository
from marionette.application.protocols.types import CharacterId
from marionette.domain.exceptions import CharacterIsAbandoned
from marionette.domain.policies.character_policy import CharacterPolicy
from marionette.domain.statuses import CharacterStatus


class BanCharacterUseCase:
    def __init__(self, transaction: Transaction, character_repo: CharacterRepository) -> None:
        self._transaction = transaction
        self._repository = character_repo

    async def ban(self, character_id: CharacterId) -> None:
        async with self._transaction:
            character = await self._repository.get_by_character_id(character_id=character_id)
            CharacterPolicy.ensure_character_exists(character=character, expected_name=str(character_id))

            assert character is not None
            if character.status == CharacterStatus.ABANDONED:
                raise CharacterIsAbandoned()

            character.status = CharacterStatus.ABANDONED

            await self._transaction.commit()
