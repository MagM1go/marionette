from marionette.presentation.discord.bootstrap import build_discord_client


def main() -> None:
    bot = build_discord_client()
    bot.run()
