import random
from dataclasses import dataclass
from datetime import UTC, datetime

from marionette.application.protocols import Transaction
from marionette.domain.entities.character import Character
from marionette.domain.policies.paparazzi_policy import PaparazziPolicy
from marionette.domain.services.rating_service import RatingService


@dataclass
class PaparazziExposeData:
    exposed_character_name: str
    expose_channel_id: int


class PaparazziUseCase:
    def __init__(self, rating_service: RatingService, transaction: Transaction) -> None:
        self._service = rating_service
        self._transaction = transaction

    async def expose(self, character: Character) -> PaparazziExposeData | None:
        PaparazziPolicy.ensure_character_in_location(character)
        if character.entered_channel_id is None:
            return None

        now = datetime.now(UTC)
        if not character.can_be_exposed(now) or not PaparazziPolicy.is_exposed(random.random()):
            return None

        new_char_rating, loss = PaparazziPolicy.calculate_character_rating(self._service, character)

        async with self._transaction as transaction:
            character.expose_to_paparazzi(new_char_rating, now)

            if character.agency_id:
                new_agency_rating = PaparazziPolicy.calculate_agency_rating(
                    self._service, character, loss
                )
                PaparazziPolicy.ensure_character_in_agency(character)

                character.agency.rating = new_agency_rating

            await transaction.commit()

        return PaparazziExposeData(
            exposed_character_name=character.name,
            expose_channel_id=character.entered_channel_id,
        )
