from dishka import Provider, Scope, provide

from marionette.application.usecases.entrance_usecase import EntranceUseCase
from marionette.application.usecases.exit_usecase import ExitUseCase
from marionette.application.usecases.moderation_usecase import ModerationUseCase
from marionette.application.usecases.onboarding.accept_onboarding_rules_usecase import AcceptOnboardingRulesUseCase
from marionette.application.usecases.onboarding.complete_onboarding_usecase import CompleteOnboardingUseCase
from marionette.application.usecases.onboarding.move_onboarding_to_intro_usecase import MoveOnboardingToIntroUseCase
from marionette.application.usecases.onboarding.move_onboarding_to_rules_usecase import MoveOnboardingToRulesUseCase
from marionette.application.usecases.onboarding.reset_onboarding_usecase import OnboardingResetUseCase
from marionette.application.usecases.onboarding.start_onboarding_usecase import StartOnboardingUseCase
from marionette.application.usecases.paparazzi_usecase import PaparazziUseCase
from marionette.application.usecases.season_reset_usecase import SeasonResetUseCase
from marionette.domain.services.rating_service import RatingService
from marionette.presentation.discord.ui.onboarding.dispatcher import OnboardingActionDispatcher

from marionette.application.usecases.register_usecase import RegisterUseCase


class UseCaseProvider(Provider):
    scope = Scope.REQUEST

    rating_service = provide(RatingService)

    paparazzi_usecase = provide(PaparazziUseCase)
    start_onboarding_usecase = provide(StartOnboardingUseCase)
    move_onboarding_to_intro_usecase = provide(MoveOnboardingToIntroUseCase)
    move_onboarding_to_rules_usecase = provide(MoveOnboardingToRulesUseCase)
    accept_onboarding_rules_usecase = provide(AcceptOnboardingRulesUseCase)
    complete_onboarding_usecase = provide(CompleteOnboardingUseCase)
    onboarding_reset_usecase = provide(OnboardingResetUseCase)
    onboarding_action_dispatcher = provide(OnboardingActionDispatcher)
    entrance_usecase = provide(EntranceUseCase)
    exit_usecase = provide(ExitUseCase)
    moderation_usecase = provide(ModerationUseCase)
    season_reset_usecase = provide(SeasonResetUseCase)
    register_usecase = provide(RegisterUseCase)
