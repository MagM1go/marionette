from marionette.domain.permissions.permission import Permission


class IgnoreEntrancePermission(Permission):
    @staticmethod
    def code() -> str:
        return "permissions.ignore_entrace"
