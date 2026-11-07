class PromotePresenter:
    @staticmethod
    def present(user_mention: str, role: str) -> str:
        return f"{user_mention} вступил в права `{role}`"
