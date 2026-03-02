from rest_framework import generics
from rest_framework.exceptions import NotFound, PermissionDenied
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.content.models import Article, Event, Page

from .serializers import ArticleSerializer, EventSerializer, GalleryItemSerializer, PageSerializer
from .utils import validate_preview_token


class PublicPageDetailView(generics.RetrieveAPIView):
    serializer_class = PageSerializer
    lookup_field = 'slug'

    def get_queryset(self):
        return Page.objects.filter(is_published=True)


class PublicArticleListView(generics.ListAPIView):
    serializer_class = ArticleSerializer

    def get_queryset(self):
        return Article.objects.filter(is_published=True)


class PublicArticleDetailView(generics.RetrieveAPIView):
    serializer_class = ArticleSerializer
    lookup_field = 'slug'

    def get_queryset(self):
        return Article.objects.filter(is_published=True)


class PublicEventListView(generics.ListAPIView):
    serializer_class = EventSerializer

    def get_queryset(self):
        return Event.objects.filter(is_published=True)


class PublicGalleryView(APIView):
    def get(self, request):
        items = []
        for article in Article.objects.filter(is_published=True, show_in_gallery=True):
            items.append({
                'title': article.title,
                'slug': article.slug,
                'type': 'article',
                'cover_image': article.cover_image,
                'youtube_video_id': article.youtube_video_id,
            })
        for event in Event.objects.filter(is_published=True, show_in_gallery=True):
            items.append({
                'title': event.title,
                'slug': event.title,
                'type': 'event',
                'cover_image': event.cover_image,
                'youtube_video_id': event.youtube_video_id,
            })
        return Response(GalleryItemSerializer(items, many=True).data)


class PreviewArticleView(generics.RetrieveAPIView):
    serializer_class = ArticleSerializer
    lookup_field = 'slug'

    def get_queryset(self):
        return Article.objects.all()

    def get_object(self):
        slug = self.kwargs.get('slug')
        token = self.request.query_params.get('token', '')
        if not validate_preview_token('article', slug, token):
            raise PermissionDenied('Token de preview inválido.')
        try:
            return self.get_queryset().get(slug=slug)
        except Article.DoesNotExist as exc:
            raise NotFound('Artigo não encontrado.') from exc
