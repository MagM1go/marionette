from collections.abc import Sequence

from marionette.application.protocols import CharacterRepository
from marionette.application.protocols.types import UserId
from marionette.domain.entities.character import Character


class CharacterQueries:
    def __init__(self, repository: CharacterRepository) -> None:
        self._repository = repository

    async def get_character(self, user_id: UserId, name: str) -> Character | None:
        return await self._repository.get_by_user_id_and_name(user_id, name)

    async def get_user_characters(self, user_id: UserId) -> Sequence[Character]:
        return await self._repository.get_all_characters_by_user_id(user_id)
