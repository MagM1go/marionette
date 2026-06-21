from dataclasses import dataclass
from datetime import datetime

from marionette.application.protocols import CharacterRepository, Transaction
from marionette.application.protocols.types import UserId
from marionette.domain.policies.character_policy import CharacterPolicy

from marionette.domain.roles import Roles


@dataclass
class CharacterInfo:
    name: str
    role: Roles
    biography: str
    birthday: datetime
    rating: int
    is_in_location: bool
    agency_id: int | None
    

class CharacterLookupByUserUseCase:
    """Searching character by his name or ID"""

    def __init__(self, transaction: Transaction, character_repo: CharacterRepository) -> None:
        self._transaction = transaction
        self._repository = character_repo

    async def lookup(self, user_id: UserId, character_name: str) -> CharacterInfo:
        async with self._transaction:
            character = await self._repository.get_by_user_id_and_name(user_id=user_id, name=character_name)
            CharacterPolicy.ensure_character_exists(character, character_name)

            assert character is not None
            return CharacterInfo(
                name=character.name,
                role=character.role,
                biography=character.biography,
                birthday=character.birthday,
                rating=character.rating,
                is_in_location=character.is_active,
                agency_id=character.agency_id
            )
