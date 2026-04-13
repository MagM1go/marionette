import crescent
import hikari

from marionette.bootstrap.config import config
from marionette.bootstrap.di.container import CrescentContainer
from marionette.presentation.discord.exceptions import DiscordException
from marionette.presentation.discord.ui.onboarding.publisher import OnboardingPublisher
from marionette.presentation.discord.ui.onboarding.registry import onboarding_registry
from marionette.presentation.discord.ui.onboarding.view_registry import OnboardingViewRegistry

plugin = crescent.Plugin[hikari.GatewayBot, CrescentContainer]()


@plugin.include
@crescent.command(
    guild=config.discord.main_guild_id,
    name="initialize",
    description="Административная команда для инициализации онбординга",
    default_member_permissions=hikari.Permissions.ADMINISTRATOR,
)
class InitializeOnboardingCommand:
    screen = crescent.option(
        str, choices=[(screen.screen_id, screen.screen_id) for screen in onboarding_registry.screens]
    )

    async def callback(self, ctx: crescent.Context) -> None:
        if ctx.guild is None:
            raise DiscordException()

        screen = onboarding_registry.get_by_id(self.screen)
        if screen is None:
            raise DiscordException()

        await OnboardingPublisher(ctx.app.rest).publish(screen)


@plugin.include
@crescent.event
async def on_startup(_: hikari.StartedEvent) -> None:
    OnboardingViewRegistry(plugin.model.component_client).register_persistent_views(
        onboarding_registry
    )
