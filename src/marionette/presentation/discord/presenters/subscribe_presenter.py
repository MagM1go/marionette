class SubscribePresenter:
    @staticmethod
    def present(character_name: str) -> str:
        return f"Вы подписались на... **{character_name}**\nСерьёзно? Выбор ваш, не мешаю."
