class DomainException(Exception):
    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(message)


class CharacterNotFound(DomainException): ...


class CharacterLocked(DomainException): ...
