from marionette.domain.permissions.permission import Permission


class ApproveCharacterPermission(Permission):
    @staticmethod
    def code() -> str:
        return "permissions.approve_character"
