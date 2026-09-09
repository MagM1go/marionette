import typing as t

from marionette.domain.entities.thread import Thread


class ThreadRepository(t.Protocol):
    def create(self, name: str, description: str) -> Thread: ...
