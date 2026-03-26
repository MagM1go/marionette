from marionette.application.protocols import IAgencyRepository, ICharacterRepository
from marionette.domain.policies.season_reset_policy import SeasonResetPolicy


class SeasonResetUseCase:
    """
    | До сброса  | После сброса |
    | ---------- | ------------ |
    | 0-99       | 0            |
    | 100-299    | 25           |
    | 300-499    | 70           |
    | 500-699    | 150          |
    | 700-899    | 200          |
    | 900-999    | 300          |
    | 1000+      | 400          |
    """

    def __init__(
        self,
        character_repo: ICharacterRepository,
        agency_repo: IAgencyRepository,
    ) -> None:
        self._character_repo = character_repo
        self._agency_repo = agency_repo

        self.repos = [self._character_repo, self._agency_repo]

    async def execute(self) -> None:
        for repo in self.repos:
            for entity in await repo.get_all():  # type: ignore
                entity.rating = SeasonResetPolicy.get_reset_rating(entity.rating)
