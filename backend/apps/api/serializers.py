from rest_framework import serializers

from apps.content.models import Article, Event, Page


class PageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Page
        fields = ('title', 'slug', 'content', 'updated_at')


class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = (
            'title', 'slug', 'summary', 'content', 'cover_image', 'youtube_video_id',
            'show_in_gallery', 'published_at', 'created_at', 'updated_at'
        )


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = (
            'title', 'description', 'start_date', 'end_date', 'location',
            'cover_image', 'youtube_video_id', 'show_in_gallery'
        )


class GalleryItemSerializer(serializers.Serializer):
    title = serializers.CharField()
    slug = serializers.CharField()
    type = serializers.CharField()
    cover_image = serializers.CharField()
    youtube_video_id = serializers.CharField(allow_blank=True, allow_null=True)
