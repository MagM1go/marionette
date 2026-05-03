from collections.abc import Sequence
from datetime import datetime
from typing import Protocol

from marionette.application.protocols.types import CharacterId, UserId
from marionette.domain.entities.character import Character
from marionette.domain.roles import Roles


class CharacterRepository(Protocol):
    """Хранилище персонажей игроков."""

    def create(
        self,
        user_id: UserId,
        name: str,
        role: Roles,
        birthday: datetime,
        biography: str
    ) -> Character | None:
        """Создаёт нового персонажа.

        Args:
            user_id: Discord ID пользователя.
            name: Имя персонажа.
            role: Роль персонажа в индустрии.
            birthday: Дата рождения персонажа. Используется для проверки доступа к NSFW каналам.
            biography: Биография персонажа

        Returns:
            Созданный персонаж или None, если персонаж с таким именем уже существует у пользователя.
        """

    async def get_all(self) -> Sequence[Character]:
        """Возвращает всех персонажей всех игроков."""
        ...

    async def get_by_user_id_and_name(self, user_id: UserId, name: str) -> Character | None:
        """Возвращает персонажа пользователя по имени.

        Args:
            name: Имя персонажа.
            user_id: Discord ID пользователя.

        Returns:
            Персонаж или None, если не найден.
        """

    async def get_all_characters_by_user_id(self, user_id: UserId) -> Sequence[Character]:
        """Возвращает всех персонажей пользователя.

        Args:
            user_id: Discord ID пользователя.

        Returns:
            Список персонажей. Пустой список если персонажей нет.
        """
        ...

    async def get_by_character_id(self, character_id: CharacterId) -> Character | None:
        """Возвращает персонажа по его ID.

        Args:
            character_id: ID персонажа в базе данных.is_active

        Returns:
            Персонаж или None, если не найден.
        """

    async def get_entered_character_by_user_id(self, user_id: UserId) -> Character | None:
        """Возвращает активного персонажа пользователя

        Args:
            user_id: Discord ID пользователя.

        Returns:
            Персонаж или None, если не найден.
        """

    async def delete(self, character: Character) -> None:
        """Удаляет персонажа.

        Args:
            character: Персонаж игрока
        """
        ...
