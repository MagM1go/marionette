from typing import Protocol

from marionette.application.protocols import UserId
from marionette.domain.entities.report import Report


class ReportRepository(Protocol):
    def create(self, issuer_id: UserId, reported_id: UserId, reason: str) -> Report:
        """Создаёт запись жалобы"""
        ...
