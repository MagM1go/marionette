from marionette.application.protocols import CharacterRepository
from marionette.application.protocols.transaction import Transaction
from marionette.application.protocols.types import CharacterId
from marionette.domain.policies.character_policy import CharacterPolicy
from marionette.domain.statuses import CharacterStatus


class DeclineCharacterUseCase:
    def __init__(self, transaction: Transaction, character_repo: CharacterRepository) -> None:
        self._repository = character_repo
        self._transaction = transaction

    async def decline(self, character_id: CharacterId) -> str:
        """Всегда возвращает имя отклонённого персонажа"""

        async with self._transaction:
            character = await self._repository.get_by_character_id(character_id=character_id)
            CharacterPolicy.ensure_character_exists(character=character, expected_name=str(character_id))

            assert character is not None
            CharacterPolicy.ensure_character_can_be_judged(character=character)

            character.status = CharacterStatus.ABANDONED

            await self._transaction.commit()

            return character.name
