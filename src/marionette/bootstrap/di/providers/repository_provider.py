from dishka import Provider, Scope, provide

from marionette.application.protocols import AgencyRepository, CharacterRepository, OnboardingRepository, SubscriptionRepository, VoteRepository
from marionette.application.protocols.repositories.report_repository import ReportRepository
from marionette.application.protocols.repositories.staff_repository import StaffRepository
from marionette.infrastructure.repositories.agency_repository import SqlAlchemyAgencyRepository
from marionette.infrastructure.repositories.character_repository import SqlAlchemyCharacterRepository
from marionette.infrastructure.repositories.onboarding_repository import SqlAlchemyOnboardingRepository
from marionette.infrastructure.repositories.report_repository import SqlAlchemyReportRepository
from marionette.infrastructure.repositories.staff_repository import SqlAlchemyStaffRepository
from marionette.infrastructure.repositories.subscription_repository import SqlAlchemySubscriptionRepository
from marionette.infrastructure.repositories.vote_repository import SqlAlchemyVoteRepository


class RepositoryProvider(Provider):
    scope = Scope.REQUEST

    character_repository = provide(SqlAlchemyCharacterRepository, provides=CharacterRepository)
    agency_repository = provide(SqlAlchemyAgencyRepository, provides=AgencyRepository)
    onboarding_repository = provide(SqlAlchemyOnboardingRepository, provides=OnboardingRepository)
    vote_repository = provide(SqlAlchemyVoteRepository, provides=VoteRepository)
    follower_repository = provide(SqlAlchemySubscriptionRepository, provides=SubscriptionRepository)
    staff_repository = provide(SqlAlchemyStaffRepository, provides=StaffRepository)
    report_repository = provide(SqlAlchemyReportRepository, provides=ReportRepository)
