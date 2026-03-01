from marionette.domain.entities.character import Character
from marionette.domain.exceptions import CharacterLocked, CharacterNotFound
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

        if character.entranced_channel_id:
            raise CharacterLocked(
                f"Персонаж уже активен в <#{character.entranced_channel_id}>! "
                + "Чтобы выйти, воспользуйтесь командой `/exit`"
            )
            
        characters = await self.character_repo.get_all_characters_by_user_id(user_id)
        if any(с.entranced_channel_id is not None for с in characters):
            raise CharacterLocked(
                "У вас уже есть активный персонаж! Проверьте, кто это: `/profile characters active`"
            )

        await self.character_repo.set_timeline(character, thread_id)
        return character
