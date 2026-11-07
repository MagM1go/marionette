from marionette.application.protocols import CharacterRepository, UserId
from marionette.application.protocols.repositories.staff_repository import StaffRepository
from marionette.domain.permissions.ignore_entrance import IgnoreEntrancePermission
from marionette.domain.policies.moderation_policy import ModerationPolicy


# TODO: Избавиться или перенести, но это не будет долго жить
class DeleteOfftopicMessageUseCase:
    def __init__(self, character_repo: CharacterRepository, staff_repository: StaffRepository) -> None:
        self._character_repository = character_repo
        self._staff_repository = staff_repository

    async def execute(
        self,
        *,
        user_id: int,
        channel_id: int,
        message_content: str | None,
    ) -> bool:
        staff = await self._staff_repository.get_by_user_id(user_id=UserId(user_id))
        if staff and staff.role.has_permission(IgnoreEntrancePermission):
            return True

        if not message_content:
            return False

        if not ModerationPolicy.should_delete_message(message_content):
            return False

        entered_character = await self._character_repository.get_entered_character_by_user_id(UserId(user_id))
        entered_channel_id = entered_character.entered_channel_id if entered_character else None

        return entered_channel_id != channel_id
