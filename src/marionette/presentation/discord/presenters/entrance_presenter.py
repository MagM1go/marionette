class EntryExitPresenter:
    exit_message: str = "Вы покинули локацию. Виу-виу..."
    
    @staticmethod
    def present_entry(location_id: int) -> str:
        return f"Вы успешно присоединились к локации! Добро пожаловать: <#{location_id}>"
