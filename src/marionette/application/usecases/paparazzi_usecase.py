import random
from datetime import UTC, datetime

from marionette.application.dto.paparazzi import PaparazziExposeData
from marionette.domain.entities.character import Character
from marionette.domain.policies.paparazzi_policy import PaparazziPolicy
from marionette.domain.services.rating_service import RatingService


class PaparazziUseCase:
    def __init__(self, rating_service: RatingService) -> None:
        self.rating_service = rating_service

    async def expose(self, character: Character) -> PaparazziExposeData | None:
        PaparazziPolicy.ensure_character_in_location(character)

        if not character.can_be_exposed():
            return None

        if not PaparazziPolicy.is_exposed(random.random()):
            return None

        new_char_rating, loss = PaparazziPolicy.calculate_character_rating(
            self.rating_service, character
        )

        character.apply_paparazzi_incident(new_char_rating)

        if character.agency_id:
            new_agency_rating = PaparazziPolicy.calculate_agency_rating(
                self.rating_service, character, loss
            )
            character.agency.rating = new_agency_rating

        assert character.entranced_channel_id is not None
        return PaparazziExposeData(
            exposed_character_name=character.name,
            expose_channel_id=character.entranced_channel_id,
        )
