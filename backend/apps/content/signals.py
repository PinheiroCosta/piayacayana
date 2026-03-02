from django.apps import apps
from django.db.models.signals import post_migrate


def create_default_groups(sender, **kwargs):
    if sender.name != "apps.content":
        return
    Group = apps.get_model("auth", "Group")
    Group.objects.get_or_create(name="Administrador")
    Group.objects.get_or_create(name="Editor")


post_migrate.connect(create_default_groups)
