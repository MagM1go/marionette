from enum import StrEnum


class Roles(StrEnum):
    IDOL = "Idol"
    ACTOR = "Actor"
    MANGAKA = "Mangaka"
    EDITOR = "Editor"
    WRITER = "Writer"
    AGENT = "Agent"
    LAWYER = "Lawyer"
    MEDICINE = "Medicine"
    STYLIST = "Stylist"
    MAFIA = "Mafia"


class AgencyRoles(StrEnum):
    DIRECTOR = "Agency Director"
    MANAGER = "Agency Manager"
