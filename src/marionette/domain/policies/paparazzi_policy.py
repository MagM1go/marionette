import typing as t

from marionette.domain.exceptions import CharacterNotInLocation
from marionette.domain.services.rating_service import RatingChangeReason, RatingService

if t.TYPE_CHECKING:
    from marionette.domain.entities.character import Character


class PaparazziPolicy:
    ONE_DAY: int = 60 * 60 * 24
    EXPOSE_CHANCE: tuple[float, float] = (0.2, 0.24)

    @staticmethod
    def ensure_character_in_location(character: Character) -> None:
        if not character.entranced_channel_id:
            raise CharacterNotInLocation()

    @classmethod
    def is_exposed(cls, random_value: float) -> bool:
        return cls.EXPOSE_CHANCE[0] < random_value < cls.EXPOSE_CHANCE[1]

    @classmethod
    def calculate_character_rating(
        cls, service: RatingService, character: Character
    ) -> tuple[int, int]:
        character_new_rating = service.dec_character_rating(
            rating=character.rating, reason=RatingChangeReason.NEWS_NEGATIVE
        )
        character_loss = character.rating - character_new_rating

        return character_new_rating, character_loss

    @classmethod
    def calculate_agency_rating(
        cls, service: RatingService, character: Character, character_loss: int
    ) -> int:
        return service.dec_agency_rating_from_member(
            agency_rating=character.agency.rating,
            character_loss=character_loss,
        )

    @staticmethod
    def recalculate_exposed_rating(service: RatingService, character: Character) -> None:
        character_new_rating, character_loss = PaparazziPolicy.calculate_character_rating(
            service, character
        )

        if character.agency_id:
            character.agency.rating = PaparazziPolicy.calculate_agency_rating(
                service, character, character_loss
            )

        character.rating = character_new_rating
