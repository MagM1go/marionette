from marionette.application.protocols import IAgencyRepository, ICharacterRepository


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
        self.character_repo = character_repo
        self.agency_repo = agency_repo

    async def execute(self) -> None:
        def reset_bounds(rating: int) -> int:
            bounds = [
                (100, 0),
                (300, 25),
                (500, 70),
                (700, 150),
                (900, 200),
                (1000, 300),
            ]
            for max_value, bound in bounds:
                if rating < max_value:
                    return bound
            return 400

        for repo in [self.agency_repo, self.character_repo]:
            for entity in await repo.get_all(): # type: ignore
                entity.rating = reset_bounds(entity.rating)
