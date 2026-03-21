from marionette.application.dto.entrance import EntryExitData
from marionette.application.protocols import ChannelId, ICharacterRepository, UserId
from marionette.domain.exceptions import (
    AlreadyInLocation,
    AnotherCharacterIsActive,
    CharacterNotFound,
)


class EntranceUseCase:
    def __init__(self, character_repo: ICharacterRepository) -> None:
        self.character_repo = character_repo

    async def execute(
        self, user_id: int, character_name: str, thread_id: int
    ) -> EntryExitData:
        character = await self.character_repo.get_by_user_id_and_name(
            UserId(user_id), character_name
        )
        if not character:
            raise CharacterNotFound(character_name)

        if character.entranced_channel_id:
            raise AlreadyInLocation(character.entranced_channel_id)

        entranced = await self.character_repo.get_entranced_character_by_user_id(
            UserId(user_id)
        )
        if entranced:
            raise AnotherCharacterIsActive(entranced.name)

        await self.character_repo.set_location(character, ChannelId(thread_id))
        return EntryExitData(location_id=thread_id)
