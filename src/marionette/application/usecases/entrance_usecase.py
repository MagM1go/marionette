from marionette.application.dto.result import Result
from marionette.domain.services.roleplay_service import RoleplayService


class EntranceUseCase:
    def __init__(self, roleplay_service: RoleplayService) -> None:
        self.roleplay_service = roleplay_service

    async def execute(
        self, user_id: int, character_name: str, thread_id: int
    ) -> Result:
        await self.roleplay_service.entrance_location(
            user_id=user_id, character_name=character_name, thread_id=thread_id
        )
        return Result(f"Вы успешно присоединились к таймлайну! Добро пожаловать: <#{thread_id}>")
