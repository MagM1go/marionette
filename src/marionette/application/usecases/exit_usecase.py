from marionette.application.dto.entrance import EntryExitData
from marionette.application.protocols import ICharacterRepository, UserId
from marionette.domain.exceptions import (
    CharacterNotFound,
    CharacterNotInLocation,
    WrongChannel,
)


class ExitUseCase:
    def __init__(self, character_repo: ICharacterRepository) -> None:
        self.character_repo = character_repo

    async def execute(self, user_id: int, character_name: str, thread_id: int) -> EntryExitData:
        character = await self.character_repo.get_by_user_id_and_name(
            UserId(user_id), character_name
        )
        if not character:
            raise CharacterNotFound(character_name)

        if not character.entranced_channel_id:
            raise CharacterNotInLocation()

        if thread_id != character.entranced_channel_id:
            raise WrongChannel(character.entranced_channel_id)

        await self.character_repo.set_location(character, None)
        return EntryExitData(location_id=thread_id)
