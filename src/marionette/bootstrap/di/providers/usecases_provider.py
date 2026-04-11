from dishka import Provider, Scope, provide

from marionette.application.usecases.entrance_usecase import EntranceUseCase
from marionette.application.usecases.exit_usecase import ExitUseCase
from marionette.application.usecases.moderation_usecase import ModerationUseCase
from marionette.application.usecases.onboarding_reset_usecase import OnboardingResetUseCase
from marionette.application.usecases.onboarding_usecase import OnboardingUseCase
from marionette.application.usecases.paparazzi_usecase import PaparazziUseCase
from marionette.application.usecases.season_reset_usecase import SeasonResetUseCase
from marionette.domain.services.rating_service import RatingService


class UseCaseProvider(Provider):
    scope = Scope.REQUEST

    rating_service = provide(RatingService)

    paparazzi_usecase = provide(PaparazziUseCase)
    onboarding_usecase = provide(OnboardingUseCase)
    onboarding_reset_usecase = provide(OnboardingResetUseCase)
    entrance_usecase = provide(EntranceUseCase)
    exit_usecase = provide(ExitUseCase)
    moderation_usecase = provide(ModerationUseCase)
    season_reset_usecase = provide(SeasonResetUseCase)
