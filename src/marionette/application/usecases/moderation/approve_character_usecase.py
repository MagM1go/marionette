from dataclasses import dataclass

from marionette.application.protocols import CharacterRepository
from marionette.application.protocols.transaction import Transaction
from marionette.application.protocols.types import CharacterId
from marionette.domain.entities.character import CharacterStatus
from marionette.domain.policies.character_policy import CharacterPolicy
from marionette.domain.roles import Roles


@dataclass
class ApproveDTO:
    name: str
    role: Roles


class ApproveCharacterUseCase:
    def __init__(self, transaction: Transaction, character_repo: CharacterRepository) -> None:
        self._repository = character_repo
        self._transaction = transaction

    async def approve(self, character_id: CharacterId, biography: str) -> ApproveDTO:
        """Всегда возвращает имя одобренного персонажа"""

        async with self._transaction:
            character = await self._repository.get_by_character_id(character_id=character_id)
            CharacterPolicy.ensure_character_exists(character=character, expected_name=str(character_id))

            assert character is not None
            CharacterPolicy.ensure_character_can_be_judged(character=character)

            character.biography = biography
            character.status = CharacterStatus.IS_ACTIVE

            await self._transaction.commit()

            return ApproveDTO(character.name, character.role)
