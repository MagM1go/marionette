import random

from marionette.application.dto.paparazzi import PaparazziExposeData
from marionette.application.protocols import ICooldownRepository
from marionette.domain.entities.character import Character
from marionette.domain.services.rating_service import RatingChangeReason, RatingService


class PaparazziUseCase:
    ONE_DAY: int = 60 * 60 * 24
    EXPOSE_CHANCE: tuple[float, float] = (0.2, 0.37)

    def __init__(
        self,
        rating_service: RatingService,
        cooldown_repo: ICooldownRepository,
    ) -> None:
        self.rating_service = rating_service
        self.cooldown_repo = cooldown_repo

    async def expose(self, character: Character) -> PaparazziExposeData | None:
        if not character.entranced_channel_id:
            raise ValueError("Персонаж должен находиться в локации.")

        cd_key = f"cooldown:{character.user_id}:{character.id}"
        if await self.cooldown_repo.is_on_cooldown(cd_key):
            return None

        if not (self.EXPOSE_CHANCE[0] < random.random() < self.EXPOSE_CHANCE[1]):
            return None

        character_new_rating = self.rating_service.dec_character_rating(
            rating=character.rating, reason=RatingChangeReason.NEWS_NEGATIVE
        )
        character_loss = character.rating - character_new_rating

        if character.agency_id:
            character.agency.rating = self.rating_service.dec_agency_rating_from_member(
                agency_rating=character.agency.rating,
                character_loss=character_loss,
            )

        character.rating = character_new_rating

        await self.cooldown_repo.set_cooldown(cd_key, self.ONE_DAY)

        return PaparazziExposeData(
            exposed_character_name=character.name,
            expose_channel_id=character.entranced_channel_id,
        )
