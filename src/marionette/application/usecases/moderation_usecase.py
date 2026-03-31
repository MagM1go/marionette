from marionette.application.protocols import CharacterRepository, UserId
from marionette.domain.policies.moderation_policy import ModerationPolicy


class ModerationUseCase:
    def __init__(self, character_repo: CharacterRepository) -> None:
        self._repository = character_repo

    async def execute(
        self,
        *,
        user_id: int,
        channel_id: int,
        message_content: str | None
    ) -> bool:
        if not message_content:
            return False

        entranced_character = await self._repository.get_entranced_character_by_user_id(
            UserId(user_id)
        )
        entranced_channel_id = (
            entranced_character.entranced_channel_id if entranced_character else None
        )

        if entranced_channel_id == channel_id:
            return False

        return ModerationPolicy.should_delete_message(message_content)
