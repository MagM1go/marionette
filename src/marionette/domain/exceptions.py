class DomainException(Exception): ...


class CharacterNotFound(DomainException):
    def __init__(self, name: str) -> None:
        super().__init__()
        self.name = name


class AlreadyEntranced(DomainException):
    def __init__(self, channel_id: int) -> None:
        super().__init__()
        self.channel_id = channel_id


class AnotherCharacterIsActive(DomainException):
    def __init__(self, character_name: str) -> None:
        super().__init__()
        self.character_name = character_name


class CharacterNotEntranced(DomainException): ...


class WrongChannel(DomainException): 
    def __init__(self, expected_channel_id: int) -> None:
        super().__init__()
        self.expected_channel_id = expected_channel_id
