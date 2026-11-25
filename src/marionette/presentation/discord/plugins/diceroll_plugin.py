import random

import crescent
import hikari

from marionette.bootstrap.config import config
from marionette.bootstrap.di.container import CrescentContainer

plugin = crescent.Plugin[hikari.GatewayBot, CrescentContainer]()


# TODO: перенести в домен надо будет
@plugin.include
@crescent.command(name="roll", description="Бросить кубик... или не совсем кубик", guild=config.discord.guild.main)
class DIceRollPlugin:
    expression = crescent.option(str, "Например: d10 / 3d10 t2 / 4d10 k3")

    def parse_roll_rule(self, expression: str) -> tuple[int, int]:
        count, user_roll = expression.split("d", 1)
        # second_arg = self.expression.split("")[1]
        if int(user_roll) < 1:
            return 1, 1
            
        return int(count) if count.isdigit() else 1, int(user_roll)

    async def callback(self, ctx: crescent.Context) -> None:
        rolls = self.parse_roll_rule(self.expression)
        results = [str(random.randint(1, rolls[1])) for _ in range(rolls[0])]
        await ctx.respond(", ".join(results))
