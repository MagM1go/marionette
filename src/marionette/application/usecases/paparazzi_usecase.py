import random

from marionette.application.dto.paparazzi import PaparazziExposeData
from marionette.application.protocols import CharacterId, ICooldownRepository, UserId
from marionette.domain.entities.character import Character
from marionette.domain.policies.paparazzi_policy import PaparazziPolicy
from marionette.domain.services.rating_service import RatingService


class PaparazziUseCase:
    def __init__(
        self,
        rating_service: RatingService,
        cooldown_repo: ICooldownRepository,
    ) -> None:
        self.rating_service = rating_service
        self.cooldown_repo = cooldown_repo

    async def expose(self, character: Character) -> PaparazziExposeData | None:
        PaparazziPolicy.ensure_character_in_location(character)

        cooldown_key = self._make_cooldown_key(UserId(character.user_id), CharacterId(character.id))
        if await self.cooldown_repo.is_on_cooldown(cooldown_key):
            return None

        if not PaparazziPolicy.is_exposed(random.random()):
            return None

        PaparazziPolicy.recalculate_exposed_rating(self.rating_service, character)

        await self.cooldown_repo.set_cooldown(cooldown_key, PaparazziPolicy.ONE_DAY)

        assert character.entranced_channel_id is not None
        return PaparazziExposeData(
            exposed_character_name=character.name,
            expose_channel_id=character.entranced_channel_id,
        )

    def _make_cooldown_key(self, user_id: UserId, character_id: CharacterId) -> str:
        return f"cooldown:{user_id}:{character_id}"
