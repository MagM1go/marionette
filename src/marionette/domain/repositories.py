from abc import ABC, abstractmethod
from collections.abc import Sequence
from datetime import datetime

from marionette.domain.entities.agency import Agency
from marionette.domain.entities.character import Character
from marionette.domain.roles import Roles


class ICharacterRepository(ABC):
    @abstractmethod
    async def save(
        self,
        user_id: int,
        name: str,
        role: Roles,
        birthday: datetime,
        home_channel_id: int,
    ) -> Character | None:
        """Создаёт и сохраняет нового персонажа.

        Args:
            user_id: Discord ID пользователя.
            name: Имя персонажа.
            role: Роль персонажа в индустрии.
            birthday: Дата рождения персонажа. Используется для проверки доступа к NSFW каналам.

        Returns:
            Созданный персонаж или None, если персонаж с таким именем уже существует у пользователя.
        """

    @abstractmethod
    async def update(self) -> None:
        """Фиксирует изменения текущей сессии в базе данных."""

    @abstractmethod
    async def get_all(self) -> Sequence[Character]:
        """Возвращает всех персонажей всех игроков."""

    @abstractmethod
    async def set_active(self, user_id: int, name: str, is_active: bool) -> None:
        """Устанавливает активного персонажа игрока.

        Только один персонаж может быть активным одновременно. Активный персонаж
        используется для всех игровых действий: /entrance, /call и прочих команд.
        Если активный персонаж не выбран - большинство команд недоступны.

        Args:
            user_id: Discord ID пользователя.
            name: Имя персонажа которого нужно активировать/деактивировать.
            is_active: True - установить как активного, False - убирает активного персонажа.
        """

    @abstractmethod
    async def set_location(self, character: Character, channel_id: int | None) -> None:
        """Вход/выход из временной линии (РП-канала)

        Args:
            character: Объект персонажа
            channel_id: Discord ID канала
        """

    @abstractmethod
    async def get_by_user_id_and_name(
        self, user_id: int, name: str
    ) -> Character | None:
        """Возвращает персонажа пользователя по имени.

        Args:
            name: Имя персонажа.
            user_id: Discord ID пользователя.

        Returns:
            Персонаж или None, если не найден.
        """

    @abstractmethod
    async def get_all_characters_by_user_id(self, user_id: int) -> Sequence[Character]:
        """Возвращает всех персонажей пользователя.

        Args:
            user_id: Discord ID пользователя.

        Returns:
            Список персонажей. Пустой список если персонажей нет.
        """

    @abstractmethod
    async def get_by_character_id(self, character_id: int) -> Character | None:
        """Возвращает персонажа по его ID.

        Args:
            character_id: ID персонажа в базе данных.is_active

        Returns:
            Персонаж или None, если не найден.
        """
        
    @abstractmethod
    async def get_entranced_character_by_user_id(self, user_id: int) -> Character | None:
        """Возвращает канал, в котором присутствует активный персонаж
        
        Args:
            user_id: Discord ID пользователя.
        
        Returns:
            Персонаж или None, если не найден.
        """

    @abstractmethod
    async def delete_by_name_and_user_id(self, name: str, user_id: int) -> bool:
        """Удаляет персонажа пользователя по имени.

        Args:
            name: Имя персонажа.
            user_id: Discord ID пользователя.

        Returns:
            True, если персонаж удалён и False, если не найден.
        """


class IAgencyRepository(ABC):
    @abstractmethod
    async def save(
        self,
        owner_id: int,
        name: str,
    ) -> Agency | None:
        """Создаёт и сохраняет новое агентство.

        Args:
            owner_id: Discord ID владельца (директора) агентства.
            name: Название агентства.

        Returns:
            Созданное агентство или None, если агентство с таким именем уже существует.
        """

    @abstractmethod
    async def update(self) -> None:
        """Фиксирует изменения текущей сессии в базе данных."""

    @abstractmethod
    async def get_all(self) -> Sequence[Agency]:
        """Возвращает все агентства."""

    @abstractmethod
    async def get_agency_by_id(self, id: int) -> Agency | None:
        """Возвращает агентство по его ID.

        Args:
            id: ID агентства в базе данных.

        Returns:
            Агентство или None,
        """


class ICooldownRepository(ABC):
    @abstractmethod
    async def is_on_cooldown(self, key: str) -> bool: ...

    @abstractmethod
    async def set_cooldown(self, key: str, seconds: int) -> None: ...
