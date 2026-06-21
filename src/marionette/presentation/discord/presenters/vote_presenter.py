class VotePresenter:
    @staticmethod
    def present(name: str) -> str:
        return f"Вы отдали свой голос за **{name}**. Молитесь, чтобы он или она Вас не подвели."

    @staticmethod
    def present_vote_button() -> str:
        return "Голосуй. Не ошибись.\n-# Не дави на куклу.\n> извините."

    @staticmethod
    def present_vote_timeout() -> str:
        return "Вы промахнулась со сроками голосования..."
