from django.contrib.auth.models import User

from wayneapp.services import SchemaLoader
from wayneapp.services.permission_manager import PermissionManager


def process_roles(details, user, **kwargs):
    schema_loader = SchemaLoader()
    permission_manager = PermissionManager()
    if not User.objects.filter(username=user.get_username).exists():
        business_entities = schema_loader.get_all_business_entity_names()
        for business_entity in business_entities:
            permission = permission_manager.get_view_permission(business_entity)
            user.user_permissions.add(permission)
        user.is_staff = True
        user.save()
