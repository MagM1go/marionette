import typing as t


class ThreadRepository(t.Protocol):
    def create(self, name: str, description: str, )