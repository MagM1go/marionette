from marionette.application.dto.entrance import EntryExitData
from marionette.domain.services.roleplay_service import RoleplayService


class ExitUseCase:
    def __init__(self, roleplay_service: RoleplayService) -> None:
        self.roleplay_service: RoleplayService = roleplay_service

    async def execute(
        self, user_id: int, character_name: str, thread_id: int
    ) -> EntryExitData:
        await self.roleplay_service.exit_location(
            thread_id, user_id, character_name
        )
        return EntryExitData(location_id=thread_id)
