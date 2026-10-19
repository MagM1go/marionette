import attrs
import hikari

from marionette.application.protocols import UserId
from marionette.domain.entities.onboarding import OnboardingStep


@attrs.define()
class OnboardingMoveEvent(hikari.Event):
    app: hikari.RESTAware = attrs.field()

    user_id: UserId = attrs.field()
    event_name: str = attrs.field()
    step: OnboardingStep | None = attrs.field()

    interaction: hikari.ComponentInteraction = attrs.field()
