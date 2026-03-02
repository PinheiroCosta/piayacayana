from django.contrib import admin
from django.contrib.auth.models import Group, Permission
from django.core.exceptions import PermissionDenied

from .models import Article, Event, Media, Page


class PublishControlAdmin(admin.ModelAdmin):
    def get_readonly_fields(self, request, obj=None):
        readonly = list(super().get_readonly_fields(request, obj))
        if request.user.is_superuser:
            return readonly
        if not request.user.groups.filter(name='Administrador').exists():
            readonly.append('is_published')
        return readonly

    def save_model(self, request, obj, form, change):
        if 'is_published' in form.changed_data and not (
            request.user.is_superuser or request.user.groups.filter(name='Administrador').exists()
        ):
            raise PermissionDenied('Apenas administradores podem publicar conteúdo.')
        super().save_model(request, obj, form, change)


@admin.register(Page)
class PageAdmin(PublishControlAdmin):
    list_display = ('title', 'slug', 'is_published', 'updated_at')
    list_filter = ('is_published',)
    prepopulated_fields = {'slug': ('title',)}


@admin.register(Article)
class ArticleAdmin(PublishControlAdmin):
    list_display = ('title', 'slug', 'is_published', 'show_in_gallery', 'published_at')
    list_filter = ('is_published', 'show_in_gallery')
    prepopulated_fields = {'slug': ('title',)}


@admin.register(Event)
class EventAdmin(PublishControlAdmin):
    list_display = ('title', 'start_date', 'location', 'is_published', 'show_in_gallery')
    list_filter = ('is_published', 'show_in_gallery')


@admin.register(Media)
class MediaAdmin(admin.ModelAdmin):
    list_display = ('id', 'type', 'public_url', 'created_at')
    list_filter = ('type',)


def setup_groups():
    admin_group, _ = Group.objects.get_or_create(name='Administrador')
    editor_group, _ = Group.objects.get_or_create(name='Editor')

    content_permissions = Permission.objects.filter(content_type__app_label='content')
    admin_group.permissions.set(content_permissions)

    editor_perms = content_permissions.exclude(codename__startswith='delete_')
    editor_perms = editor_perms.exclude(codename__startswith='publish_')
    editor_group.permissions.set(editor_perms)
