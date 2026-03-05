class EntrancePresenter:
    @staticmethod
    def present(location_id: int) -> str:
        return f"Вы успешно присоединились к таймлайну! Добро пожаловать: <#{location_id}>"
