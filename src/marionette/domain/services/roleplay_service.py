from marionette.domain.entities.character import Character
from marionette.domain.exceptions import CharacterLocked, CharacterNotFound, CharacterNotLocked, WrongChannel
from marionette.domain.repositories import IAgencyRepository, ICharacterRepository


class RoleplayService:
    def __init__(
        self, character_repo: ICharacterRepository, agency_repo: IAgencyRepository
    ) -> None:
        self.character_repo = character_repo
        self.agency_repo = agency_repo

    async def entrance_timeline(
        self, user_id: int, character_name: str, thread_id: int
    ) -> Character | None:
        if not (character := await self.character_repo.get_by_user_id_and_name(user_id, character_name)):
            raise CharacterNotFound(
                f"У вас нет персонажа с именем **{character_name}**!"
            )

        # ВЫБРАННЫЙ персонаж может быть активен
        if character.entranced_channel_id:
            raise CharacterLocked(
                f"Персонаж уже активен в <#{character.entranced_channel_id}>! "
                + "Чтобы выйти, воспользуйтесь командой `/exit`"
            )

        # А это - любой другой персонаж может быть активен, тоже нужно проверить
        # Активный персонаж может быть всего один.
        entranced_character = await self.character_repo.get_entranced_character_by_user_id(user_id)
        if entranced_character:
            raise CharacterLocked(
                f"У вас уже есть активный персонаж! Вы, что ли, забыли про **{entranced_character.name}**?"
            )
        
        await self.character_repo.set_timeline(character, thread_id)
        return character

    async def exit_timeline(self, context_channel_id: int, user_id: int, character_name: str) -> Character:
        if not (character := await self.character_repo.get_by_user_id_and_name(user_id, character_name)):
            raise CharacterNotFound(
                f"У вас нет персонажа с именем **{character_name}**!"
            )
            
        if not character.entranced_channel_id:
            raise CharacterNotLocked("Персонаж нигде не активен! Увы...")
            
        if context_channel_id != character.entranced_channel_id:
            raise WrongChannel("Если вы хотите выйти из таймлайна, то нужно вводить команду в нём же!")
            
        await self.character_repo.set_timeline(character, None)
        return character
