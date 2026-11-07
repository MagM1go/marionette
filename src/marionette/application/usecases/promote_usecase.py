from marionette.application.protocols import UserId
from marionette.application.protocols.repositories.staff_repository import StaffRepository
from marionette.application.protocols.transaction import Transaction
from marionette.domain.entities.staff import STAFF_ROLE_TO_PERMISSIONS, StaffRoles


class PromoteStaffUseCase:
    def __init__(self, repository: StaffRepository, transaction: Transaction) -> None:
        self._repository = repository
        self._transaction = transaction

    async def promote(self, user_id: UserId, role: StaffRoles) -> None:
        async with self._transaction:
            staff = await self._repository.get_by_user_id(user_id=user_id)
            if staff is None:
                self._repository.create(user_id=user_id, role=role, permissions=STAFF_ROLE_TO_PERMISSIONS[role])
            else:
                staff.role = role
                staff.permissions = [permission.code() for permission in STAFF_ROLE_TO_PERMISSIONS[role]]

            await self._transaction.commit()
