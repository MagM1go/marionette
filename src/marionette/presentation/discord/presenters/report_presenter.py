import hikari

from marionette.bootstrap.config import config


class ReportPresenter:
    REPORT_MESSAGE_TEMPLATE = "https://discord.com/channels/{guild_id}/{channel_id}/{message_id}"

    @staticmethod
    def present(user_mention: str) -> str:
        return f"Жалоба отправлена, стукач ты е###ий. Ожидайте рассмотрения, о результате вы вряд ли узнаете напрямую. {user_mention}, не балуйся."

    @classmethod
    def present_moderator_embed(
        cls, issuer_id: int, issuer_name: str, user_id: int, user_name: str, reason: str, report_channel_id: int, report_message_id: int
    ) -> hikari.Embed:
        return hikari.Embed(title=f"Жалоба от {issuer_id} ({issuer_name}) на {user_id} ({user_name})", description=reason).add_field(
            name="Место жалобы",
            value=cls.REPORT_MESSAGE_TEMPLATE.format(
                guild_id=config.discord.guild.main,
                channel_id=report_channel_id,
                message_id=report_message_id,
            ),
        )
