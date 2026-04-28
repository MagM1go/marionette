from marionette.application.dto.entrance import EntryExitData
from marionette.application.protocols import CharacterRepository, UserId
from marionette.application.protocols.transaction import Transaction
from marionette.domain.exceptions import (
    AlreadyInLocation,
    AnotherCharacterIsActive,
    CharacterNotActive,
    CharacterNotFound,
)
from marionette.domain.statuses import CharacterStatus


class EnterLocationUseCase:
    def __init__(self, character_repo: CharacterRepository, transaction: Transaction) -> None:
        self._repository = character_repo
        self._transaction = transaction

    async def enter(self, user_id: int, character_name: str, thread_id: int) -> EntryExitData:
        async with self._transaction:
            character = await self._repository.get_by_user_id_and_name(
                UserId(user_id), character_name
            )
            
            if not character:
                raise CharacterNotFound(character_name)

            if character.status != CharacterStatus.IS_ACTIVE:
                raise CharacterNotActive(character_name)

            if character.entranced_channel_id:
                raise AlreadyInLocation(character.entranced_channel_id)

            entranced = await self._repository.get_entranced_character_by_user_id(UserId(user_id))
            if entranced:
                raise AnotherCharacterIsActive(entranced.name)

            character.set_location(thread_id)
            await self._transaction.commit()

        return EntryExitData(location_id=thread_id)
