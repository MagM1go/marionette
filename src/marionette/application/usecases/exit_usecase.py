from marionette.application.dto.entrance import EntryExitData
from marionette.application.protocols import CharacterRepository, UserId
from marionette.application.protocols.transaction import Transaction
from marionette.domain.exceptions import CharacterNotFound, CharacterNotInLocation, WrongChannel


class ExitUseCase:
    def __init__(self, character_repo: CharacterRepository, transaction: Transaction) -> None:
        self._repository = character_repo
        self._transaction = transaction

    async def execute(self, user_id: int, character_name: str, thread_id: int) -> EntryExitData:
        async with self._transaction:
            character = await self._repository.get_by_user_id_and_name(UserId(user_id), character_name)
            if not character:
                raise CharacterNotFound(character_name)
    
            if not character.entranced_channel_id:
                raise CharacterNotInLocation()
    
            if thread_id != character.entranced_channel_id:
                raise WrongChannel(character.entranced_channel_id)
    
            character.set_location(None)
            await self._transaction.commit()
            
        return EntryExitData(location_id=thread_id)
