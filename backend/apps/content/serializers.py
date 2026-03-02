from rest_framework import serializers

from .models import Article, Event, Page


class PageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Page
        fields = ["title", "slug", "content", "updated_at"]


class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = [
            "title",
            "slug",
            "summary",
            "content",
            "cover_image",
            "youtube_video_id",
            "show_in_gallery",
            "published_at",
            "updated_at",
        ]


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = [
            "title",
            "description",
            "start_date",
            "end_date",
            "location",
            "cover_image",
            "youtube_video_id",
            "show_in_gallery",
            "updated_at",
        ]


class GalleryItemSerializer(serializers.Serializer):
    type = serializers.ChoiceField(choices=["article", "event"])
    title = serializers.CharField()
    slug = serializers.CharField(required=False, allow_blank=True)
    cover_image = serializers.CharField(allow_blank=True)
    youtube_video_id = serializers.CharField(allow_blank=True)
