from dataclasses import dataclass

from marionette.application.protocols import CharacterRepository, UserId
from marionette.application.protocols.transaction import Transaction
from marionette.domain.exceptions import (
    AlreadyInLocation,
    AnotherCharacterIsActive,
    CharacterNotActive,
    CharacterNotFound,
)
from marionette.domain.statuses import CharacterStatus


@dataclass
class EnterLocationData:
    location_id: int


class EnterLocationUseCase:
    def __init__(self, character_repo: CharacterRepository, transaction: Transaction) -> None:
        self._repository = character_repo
        self._transaction = transaction

    async def enter(self, user_id: int, character_name: str, thread_id: int) -> EnterLocationData:
        async with self._transaction:
            character = await self._repository.get_by_user_id_and_name(
                UserId(user_id), character_name
            )

            if not character:
                raise CharacterNotFound(character_name)

            if character.status != CharacterStatus.IS_ACTIVE:
                raise CharacterNotActive(character_name)

            if character.entered_channel_id:
                raise AlreadyInLocation(character.entered_channel_id)

            entered = await self._repository.get_entered_character_by_user_id(UserId(user_id))
            if entered:
                raise AnotherCharacterIsActive(entered.name)

            character.set_location(thread_id)
            await self._transaction.commit()

        return EnterLocationData(location_id=thread_id)
