from marionette.domain.services.roleplay_service import RoleplayService

from marionette.application.dto.entrance import EntryExitData


class EntranceUseCase:
    def __init__(self, roleplay_service: RoleplayService) -> None:
        self.roleplay_service = roleplay_service

    async def execute(
        self, user_id: int, character_name: str, thread_id: int
    ) -> EntryExitData:
        await self.roleplay_service.entrance_location(
            user_id=user_id, character_name=character_name, thread_id=thread_id
        )

        return EntryExitData(location_id=thread_id)
