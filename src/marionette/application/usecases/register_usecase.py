from datetime import datetime

from marionette.application.protocols import CharacterRepository
from marionette.application.protocols.transaction import Transaction
from marionette.application.protocols.types import CharacterId, UserId
from marionette.domain.exceptions import TooManyCharacters
from marionette.domain.roles import Roles


class RegisterUseCase:
    def __init__(self, transaction: Transaction, repository: CharacterRepository) -> None:
        self._transaction = transaction
        self._repository = repository

    async def register(
        self,
        user_id: UserId,
        name: str,
        role: Roles,
        birthday: datetime,
        biography: str,
    ) -> CharacterId:
        async with self._transaction:
            characters = await self._repository.get_active_characters_by_user_id(user_id=user_id)

            if len(characters) >= 3:
                raise TooManyCharacters()

            character = self._repository.create(
                user_id=user_id,
                name=name,
                role=role,
                birthday=birthday,
                biography=biography,
            )

            await self._transaction.commit()

            return character.id  # type: ignore
