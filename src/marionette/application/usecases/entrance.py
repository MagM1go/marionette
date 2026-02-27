from marionette.application.dto.result import Result
from marionette.domain.services.roleplay_service import RoleplayService


class EntranceUseCase:
    def __init__(self, roleplay_service: RoleplayService) -> None:
        self.roleplay_service = roleplay_service

    async def execute(
        self, user_id: int, character_name: str, thread_id: int
    ) -> Result:
        entranced_character = await self.roleplay_service.entrance_timeline(
            user_id=user_id, character_name=character_name, thread_id=thread_id
        )
        
        if not entranced_character:
            return Result(f"У вас нет персонажа с именем **{character_name}**. Выберите персонажа из выпадающего списка")
            
        return Result(f"Вы успешно присоединились к таймлайну! Добро пожаловать: <#{thread_id}>")
