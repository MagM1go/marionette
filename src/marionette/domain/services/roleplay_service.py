from marionette.domain.entities.character import Character
from marionette.domain.repositories import IAgencyRepository, ICharacterRepository


class RoleplayService:
    def __init__(
        self, character_repo: ICharacterRepository, agency_repo: IAgencyRepository
    ) -> None:
        self.character_repo = character_repo
        self.agency_repo = agency_repo

    async def entrance_timeline(
        self, user_id: int, character_name: str, thread_id: int | None
    ) -> Character | None:
        if not (character := await self.character_repo.get_by_user_id_and_name(character_name, user_id)):
            return None

        await self.character_repo.set_timeline(character, thread_id)
        return character
