from django.contrib.auth.models import User, Group

from wayneapp.services import SchemaLoader
from wayneapp.services.permission_manager import PermissionManager


def process_roles(details, user, **kwargs):
    if not User.objects.filter(username=user.get_username).exists():
        my_group = Group.objects.get(name='business_entities_view_permission')
        user.is_staff = True
        user.groups.add(my_group)
        user.save()
