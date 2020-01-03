from herbieapp.initializers.abstract_initializer import AbstractInitializer
from herbieapp.services.permission_manager import PermissionManager


class PermissionInitializer(AbstractInitializer):

    def get_name(self) -> str:
        return 'permissions'

    def init(self):
        permission_manager = PermissionManager()
        permission_manager.create_group_and_permission_for_view_access()