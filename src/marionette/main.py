from marionette.bootstrap.app import build_discord_bot


def main() -> None:
    bot = build_discord_bot(plugins_path="src.marionette.presentation.discord.plugins")
    bot.run()
