from enum import StrEnum


class Roles(StrEnum):
    IDOL = "Айдол"
    ACTOR = "Актёр"
    MANGAKA = "Мангака"
    EDITOR = "Редактор"
    WRITER = "Писатель"
    AGENT = "Агент"
    LAWYER = "Юрист"
    MEDICINE = "Медик"
    STYLIST = "Стилист"


class HiddenRoles(StrEnum):
    MAFIA = "Мафия"


class AgencyRoles(StrEnum):
    DIRECTOR = "Директор агенства"
    MANAGER = "Менеджер агенства"
