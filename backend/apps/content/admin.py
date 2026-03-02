from django.contrib import admin
from django.contrib.auth.models import Group

from .models import Article, Event, Media, Page


class PublishRestrictedAdmin(admin.ModelAdmin):
    def get_readonly_fields(self, request, obj=None):
        readonly_fields = list(super().get_readonly_fields(request, obj))
        if request.user.groups.filter(name="Editor").exists() and not request.user.is_superuser:
            readonly_fields.append("is_published")
        return readonly_fields


@admin.register(Page)
class PageAdmin(PublishRestrictedAdmin):
    list_display = ("title", "slug", "is_published", "updated_at")


@admin.register(Article)
class ArticleAdmin(PublishRestrictedAdmin):
    list_display = ("title", "slug", "is_published", "published_at", "updated_at")


@admin.register(Event)
class EventAdmin(PublishRestrictedAdmin):
    list_display = ("title", "start_date", "end_date", "is_published")


@admin.register(Media)
class MediaAdmin(admin.ModelAdmin):
    list_display = ("id", "type", "related_article", "related_event", "created_at")


def ensure_groups() -> None:
    Group.objects.get_or_create(name="Administrador")
    Group.objects.get_or_create(name="Editor")
