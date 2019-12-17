from django.contrib.auth.models import AnonymousUser, Permission
from rest_framework.request import Request
from wayneapp.constants import ControllerConstants


class PermissionManager:

    def has_save_permission(self, business_entity: str, request: Request) -> bool:
        if type(request.user) is AnonymousUser:
            return False
        add_permission = self.get_permission_string(ControllerConstants.ADD, business_entity)
        change_permission = self.get_permission_string(ControllerConstants.CHANGE, business_entity)
        return Permission.objects \
                   .filter(user=request.user) \
                   .filter(codename__in=[add_permission, change_permission]) \
                   .count() == 2

    def has_delete_permission(self, business_entity: str, request: Request) -> bool:
        delete_permission = self.get_permission_string(ControllerConstants.DELETE, business_entity)

        return Permission.objects\
            .filter(user=request.user)\
            .filter(codename=delete_permission)\
            .exists()

    def get_view_permission(self, business_entity: str) -> Permission:
        view_permission = self.get_permission_string(ControllerConstants.VIEW, business_entity)

        return Permission.objects.get(codename=view_permission)

    def get_permission_string(self, action: str, business_entity: str) -> str:
        return action + '_' + self._remove_underscores(business_entity)

    def _remove_underscores(self, string: str) -> str:
        return string.replace('_', '')
