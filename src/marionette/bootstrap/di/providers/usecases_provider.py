from dishka import Provider, Scope, provide

from marionette.application.usecases.enter_location_usecase import EnterLocationUseCase
from marionette.application.usecases.exit_usecase import ExitLocationUseCase
from marionette.application.usecases.delete_offtopic_message_usecase import DeleteOfftopicMessageUseCase
from marionette.application.usecases.onboarding.accept_onboarding_rules_usecase import AcceptOnboardingRulesUseCase
from marionette.application.usecases.onboarding.complete_onboarding_usecase import CompleteOnboardingUseCase
from marionette.application.usecases.onboarding.move_onboarding_to_intro_usecase import MoveOnboardingToIntroUseCase
from marionette.application.usecases.onboarding.move_onboarding_to_rules_usecase import MoveOnboardingToRulesUseCase
from marionette.application.usecases.onboarding.reset_onboarding_usecase import OnboardingResetUseCase
from marionette.application.usecases.onboarding.start_onboarding_usecase import StartOnboardingUseCase
from marionette.application.usecases.paparazzi_usecase import PaparazziUseCase
from marionette.application.usecases.season_reset_usecase import ResetSeasonRatingUseCase
from marionette.domain.services.rating_service import RatingService
from marionette.presentation.discord.ui.onboarding.dispatcher import OnboardingActionDispatcher
from marionette.presentation.discord.ui.onboarding.step_assets import OnboardingStepAssets

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
    onboarding_step_assets = provide(OnboardingStepAssets)
    onboarding_action_dispatcher = provide(OnboardingActionDispatcher)
    entrance_usecase = provide(EnterLocationUseCase)
    exit_usecase = provide(ExitLocationUseCase)
    moderation_usecase = provide(DeleteOfftopicMessageUseCase)
    season_reset_usecase = provide(ResetSeasonRatingUseCase)
    register_usecase = provide(RegisterUseCase)
