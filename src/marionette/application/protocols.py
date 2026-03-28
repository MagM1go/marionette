from collections.abc import Sequence
from datetime import datetime
from typing import NewType, Protocol

from marionette.domain.entities.agency import Agency
from marionette.domain.entities.character import Character
from marionette.domain.entities.onboarding import OnboardingStep
from marionette.domain.roles import Roles

UserId = NewType("UserId", int)
RoleId = NewType("RoleId", int)
ChannelId = NewType("ChannelId", int)
CharacterId = NewType("CharacterId", int)
AgencyId = NewType("AgencyId", int)


class ICharacterRepository(Protocol):
    def create(
        self,
        user_id: UserId,
        name: str,
        role: Roles,
        birthday: datetime,
        home_channel_id: ChannelId,
    ) -> Character | None:
        """Создаёт нового персонажа.

        Args:
            user_id: Discord ID пользователя.
            name: Имя персонажа.
            role: Роль персонажа в индустрии.
            birthday: Дата рождения персонажа. Используется для проверки доступа к NSFW каналам.

        Returns:
            Созданный персонаж или None, если персонаж с таким именем уже существует у пользователя.
        """

    async def get_all(self) -> Sequence[Character]:
        """Возвращает всех персонажей всех игроков."""
        ...

    async def set_active(self, user_id: UserId, name: str, is_active: bool) -> None:
        """Устанавливает активного персонажа игрока.

        Только один персонаж может быть активным одновременно. Активный персонаж
        используется для всех игровых действий: /entrance, /call и прочих команд.
        Если активный персонаж не выбран - большинство команд недоступны.

        Args:
            user_id: Discord ID пользователя.
            name: Имя персонажа которого нужно активировать/деактивировать.
            is_active: True - установить как активного, False - убирает активного персонажа.
        """

    async def set_location(self, character: Character, channel_id: ChannelId | None) -> None:
        """Вход/выход из временной линии (РП-канала)

        Args:
            character: Объект персонажа
            channel_id: Discord ID канала
        """

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

    async def get_entranced_character_by_user_id(self, user_id: UserId) -> Character | None:
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


class IAgencyRepository(Protocol):
    def create(
        self,
        owner_id: UserId,
        name: str,
    ) -> Agency | None:
        """Создаёт новое агентство.

        Args:
            owner_id: Discord ID владельца (директора) агентства.
            name: Название агентства.

        Returns:
            Созданное агентство или None, если агентство с таким именем уже существует.
        """

    async def get_all(self) -> Sequence[Agency]:
        """Возвращает все агентства."""
        ...

    async def get_agency_by_id(self, agency_id: AgencyId) -> Agency | None:
        """Возвращает агентство по его ID.

        Args:
            agency_id: ID агентства в базе данных.

        Returns:
            Агентство или None,
        """


class IOnboardingRepository(Protocol):
    def start(self, user_id: UserId) -> None:
        """Создаёт состояние онбординга, если его ещё нет."""
        ...

    async def get_current_step(self, user_id: UserId) -> OnboardingStep | None:
        """Возвращает текущий шаг пользователя."""
        ...

    async def set_current_step(self, user_id: UserId, step: OnboardingStep) -> None:
        """Устанавливает текущий шаг пользователя."""
        ...

    async def is_complete(self, user_id: UserId) -> bool:
        """Проверяет, завершён ли онбординг."""
        ...

    async def set_complete(self, user_id: UserId) -> None:
        """Помечает онбординг как завершённый."""
        ...

    async def add_role(self, user_id: UserId, role_id: RoleId) -> None:
        """Сохраняет выданную во время онбординга роль."""
        ...

    async def remove_role(self, user_id: UserId, role_id: RoleId) -> None:
        """Удаляет сохранённую роль."""
        ...

    async def get_roles(self, user_id: UserId) -> list[RoleId]:
        """Возвращает роли, выданные пользователю во время онбординга."""
        ...

    async def reset(self, user_id: UserId) -> None:
        """Сбрасывает онбординг пользователя."""
        ...

    async def log_event(
        self,
        user_id: UserId,
        event_name: str,
        step: OnboardingStep | None = None,
        metadata: dict[str, str] | None = None,
        created_at: datetime | None = None,
    ) -> None:
        """Логирует событие онбординга."""
        ...
