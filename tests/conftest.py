import sys
from collections.abc import Callable
from datetime import datetime
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from marionette.domain.entities.agency import Agency
from marionette.domain.entities.character import Character
from marionette.domain.roles import Roles
from marionette.domain.statuses import CharacterStatus
from tests.fakes import FakeAgencyRepository, FakeCharacterRepository, FakeTransaction


@pytest.fixture
def agency_factory() -> Callable[..., Agency]:
    def factory(
        *,
        id: int = 7,
        owner_id: int = 1,
        name: str = "Starlight",
        rating: int = 400,
    ) -> Agency:
        return Agency(
            id=id,
            owner_id=owner_id,
            name=name,
            rating=rating,
        )

    return factory


@pytest.fixture
def character_factory() -> Callable[..., Character]:
    def factory(
        *,
        id: int = 10,
        user_id: int = 100,
        name: str = "Airi",
        rating: int = 100,
        entranced_channel_id: int | None = None,
        agency: Agency | None = None,
        agency_id: int | None = None,
        role: Roles = Roles.IDOL,
        biography: str = "",
        last_exposed_at: datetime | None = None,
        status: CharacterStatus = CharacterStatus.IS_ACTIVE,
    ) -> Character:
        actual_agency = agency
        actual_agency_id = agency_id
        if actual_agency is not None and actual_agency_id is None:
            actual_agency_id = actual_agency.id

        return Character(
            id=id,
            user_id=user_id,
            name=name,
            role=role,
            biography=biography,
            birthday=datetime(2000, 1, 1),
            entranced_channel_id=entranced_channel_id,
            rating=rating,
            agency=actual_agency,
            agency_id=actual_agency_id,
            is_active=False,
            is_in_performance=False,
            last_exposed_at=last_exposed_at,
            status=status,
        )

    return factory


@pytest.fixture
def character_repo_factory() -> Callable[[list[Character] | None], FakeCharacterRepository]:
    def factory(
        characters: list[Character] | None = None,
    ) -> FakeCharacterRepository:
        return FakeCharacterRepository(characters or [])

    return factory


@pytest.fixture
def agency_repo_factory() -> Callable[[list[Agency]], FakeAgencyRepository]:
    def factory(agencies: list[Agency]) -> FakeAgencyRepository:
        return FakeAgencyRepository(agencies)

    return factory


@pytest.fixture
def fake_transaction() -> FakeTransaction:
    return FakeTransaction()
