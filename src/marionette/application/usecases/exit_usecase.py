from marionette.domain.services.roleplay_service import RoleplayService

from marionette.application.dto.result import Result


class ExitUseCase:
    def __init__(self, roleplay_service: RoleplayService) -> None:
        self.roleplay_service: RoleplayService = roleplay_service
        
    async def execute(self, context_channel_id: int, user_id: int, character_name: str) -> Result:
        await self.roleplay_service.exit_timeline(context_channel_id, user_id, character_name)
        return Result(f"Вы ушли из <#{context_channel_id}>!")
