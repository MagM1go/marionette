import random

from marionette.application.dto.embed import Embed
from marionette.application.dto.result import Result
from marionette.domain.repositories import (
    IAgencyRepository,
    ICharacterRepository,
    ICooldownRepository,
)
from marionette.domain.services.rating_service import RatingChangeReason, RatingService
from marionette.domain.uow import IUnitOfWork
from marionette.presentation.colors import Color


class ExposeCharacterUseCase:
    ONE_DAY: int = 60 * 60 * 24
    EXPOSE_CHANCE: tuple[float, float] = (0.2, 0.5)
    
    def __init__(
        self,
        rating_service: RatingService,
        character_repo: ICharacterRepository,
        agency_repo: IAgencyRepository,
        uow: IUnitOfWork,
        cooldown_repo: ICooldownRepository,
    ) -> None:
        self.rating_service = rating_service
        self.character_repo = character_repo
        self.agency_repo = agency_repo
        self.uow = uow
        self.cooldown_repo = cooldown_repo

    async def expose(self, user_id: int, name: str) -> Result:
        character = await self.character_repo.get_by_user_id_and_name(
            name=name, user_id=user_id
        )

        if not character:
            return Result()

        cd_key = f"cooldown:{user_id}:{character.id}"
        if await self.cooldown_repo.is_on_cooldown(cd_key):
            return Result()

        if not (self.EXPOSE_CHANCE[0] < random.random() < self.EXPOSE_CHANCE[1]):
            return Result()

        async with self.uow as uow:
            character_new_rating = self.rating_service.dec_character_rating(
                rating=character.rating, reason=RatingChangeReason.NEWS_NEGATIVE
            )
            character_loss = character.rating - character_new_rating

            if character.agency_id:
                character.agency.rating = (
                    self.rating_service.dec_agency_rating_from_member(
                        agency_rating=character.agency.rating,
                        character_loss=character_loss,
                    )
                )

            character.rating = character_new_rating

            await uow.commit()
            await self.cooldown_repo.set_cooldown(cd_key, self.ONE_DAY)

        return Result(
            embed=Embed(
                title="📸 Папарацци не дремлют",
                description=(
                    f"Наши источники сообщают, что **{character.name}** "
                    f"был(а) замечен(а) в <#{character.entranced_channel_id}>.\n\n"
                    f"*Редакция продолжает следить за развитием событий.*"
                ),
                footer="Эксклюзив · Токийский инсайдер",
                color=Color.TABLOID,
            )
        )
