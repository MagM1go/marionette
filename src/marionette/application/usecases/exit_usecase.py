from dataclasses import dataclass

from marionette.application.protocols import CharacterRepository, UserId
from marionette.application.protocols.transaction import Transaction
from marionette.domain.exceptions import CharacterNotFound, CharacterNotInLocation, WrongChannel


@dataclass
class ExitLocationData:
    location_id: int


class ExitLocationUseCase:
    def __init__(self, character_repo: CharacterRepository, transaction: Transaction) -> None:
        self._repository = character_repo
        self._transaction = transaction

    async def exit(self, user_id: int, character_name: str, thread_id: int) -> ExitLocationData:
        async with self._transaction:
            character = await self._repository.get_by_user_id_and_name(
                UserId(user_id), character_name
            )
            if not character:
                raise CharacterNotFound(character_name)

            if not character.entered_channel_id:
                raise CharacterNotInLocation()

            if thread_id != character.entered_channel_id:
                raise WrongChannel(character.entered_channel_id)

            character.set_location(None)
            await self._transaction.commit()

        return ExitLocationData(location_id=thread_id)
