from datetime import datetime

from marionette.application.protocols.character_protocol import CharacterRepository
from marionette.application.protocols.transaction import Transaction
from marionette.application.protocols.types import UserId
from marionette.domain.roles import Roles
from marionette.domain.exceptions import TooManyCharacters


class RegisterUseCase:
    def __init__(self, transaction: Transaction, repository: CharacterRepository) -> None:
        self._transaction = transaction
        self._repository = repository

    async def execute(
        self,
        user_id: UserId,
        name: str,
        role: Roles,
        birthday: datetime,
        biography: str,
    ) -> None:
        async with self._transaction:
            characters = await self._repository.get_all_characters_by_user_id(user_id=user_id)
            
            if len(characters) >= 3:
                raise TooManyCharacters()
                    
            self._repository.create(
                user_id=user_id,
                name=name,
                role=role,
                birthday=birthday,
                biography=biography,
            )
            
            await self._transaction.commit()
