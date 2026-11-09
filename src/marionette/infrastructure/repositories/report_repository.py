from sqlalchemy.ext.asyncio import AsyncSession

from marionette.application.protocols import UserId
from marionette.application.protocols.repositories.report_repository import ReportRepository
from marionette.domain.entities.report import Report


class SqlAlchemyReportRepository(ReportRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    def create(self, issuer_id: UserId, reported_id: UserId, reason: str) -> Report:
        report = Report(issuer_id=issuer_id, reported_id=reported_id, reason=reason)
        self._session.add(report)
        return report
