from django.contrib.auth.models import Group, Permission
from django.db.models.signals import post_migrate
from django.dispatch import receiver


@receiver(post_migrate)
def create_default_groups(sender, **kwargs):
    if sender.name != 'apps.content':
        return

    admin_group, _ = Group.objects.get_or_create(name='Administrador')
    editor_group, _ = Group.objects.get_or_create(name='Editor')

    permissions = Permission.objects.filter(content_type__app_label='content')
    admin_group.permissions.set(permissions)

    editor_permissions = permissions.exclude(codename__startswith='delete_')
    editor_group.permissions.set(editor_permissions)
