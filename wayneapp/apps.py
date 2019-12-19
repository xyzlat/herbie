from django.apps import AppConfig
from django.db.models.signals import post_migrate
from wayne import settings


def create_group_for_view_permission(sender, **kwargs):
    from django.contrib.auth.models import Permission, Group
    from django.contrib.contenttypes.models import ContentType
    content_type, created = ContentType.objects.get_or_create(app_label='wayneapp', model='business_entity')
    permission, created = Permission.objects.get_or_create(
        name='Can view all business entities',
        codename='view_business_entities',
        content_type=content_type,
    )
    group, created = Group.objects.get_or_create(name='business_entities_view_group')
    group.permissions.add(permission)


class WayneappConfig(AppConfig):
    name = settings.APP_LABEL

    def ready(self):
        post_migrate.connect(create_group_for_view_permission, sender=self)
