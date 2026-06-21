from marionette.application.protocols.repositories.character_repository import CharacterRepository
from marionette.application.protocols.transaction import Transaction


# Персонажи; подписки; достижения; любимая роль; средний возраст персонажей; 
class ProfileSummaryUseCase:
    def __init__(self, transaction: Transaction, character_repo: CharacterRepository) -> None:
        self._transaction = transaction
