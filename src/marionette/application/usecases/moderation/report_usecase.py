from marionette.application.protocols import Transaction, UserId
from marionette.application.protocols.repositories.report_repository import ReportRepository


class ReportUseCase:
    def __init__(self, transaction: Transaction, repository: ReportRepository) -> None:
        self._repository = repository
        self._transaction = transaction

    async def report(self, issuer_id: UserId, reported_id: UserId, reason: str) -> None:
        async with self._transaction:
            self._repository.create(issuer_id=issuer_id, reported_id=reported_id, reason=reason)

            await self._transaction.commit()
