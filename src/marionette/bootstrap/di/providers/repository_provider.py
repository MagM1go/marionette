from dishka import Provider, Scope, provide

from marionette.application.protocols import (
    AgencyRepository,
    CharacterRepository,
    OnboardingRepository,
    VoteRepository,
)
from marionette.infrastructure.repositories.agency_repository import SqlAlchemyAgencyRepository
from marionette.infrastructure.repositories.character_repository import SqlAlchemyCharacterRepository
from marionette.infrastructure.repositories.onboarding_repository import SqlAlchemyOnboardingRepository
from marionette.infrastructure.repositories.vote_repository import SqlAlchemyVoteRepository


class RepositoryProvider(Provider):
    scope = Scope.REQUEST

    character_repository = provide(SqlAlchemyCharacterRepository, provides=CharacterRepository)
    agency_repository = provide(SqlAlchemyAgencyRepository, provides=AgencyRepository)
    onboarding_repository = provide(SqlAlchemyOnboardingRepository, provides=OnboardingRepository)
    vote_repository = provide(SqlAlchemyVoteRepository, provides=VoteRepository)
