from django.shortcuts import get_object_or_404
from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Article, Event, Page
from .serializers import ArticleSerializer, EventSerializer, GalleryItemSerializer, PageSerializer
from .utils import validate_preview_token


class PublicPageDetailView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, slug: str):
        page = get_object_or_404(Page, slug=slug, is_published=True)
        return Response(PageSerializer(page).data)


class PublicArticleListView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        qs = Article.objects.filter(is_published=True)
        return Response(ArticleSerializer(qs, many=True).data)


class PublicArticleDetailView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, slug: str):
        article = get_object_or_404(Article, slug=slug, is_published=True)
        return Response(ArticleSerializer(article).data)


class PublicEventListView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        qs = Event.objects.filter(is_published=True)
        return Response(EventSerializer(qs, many=True).data)


class PublicGalleryView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        articles = [
            {
                "type": "article",
                "title": a.title,
                "slug": a.slug,
                "cover_image": a.cover_image,
                "youtube_video_id": a.youtube_video_id,
            }
            for a in Article.objects.filter(is_published=True, show_in_gallery=True)
        ]
        events = [
            {
                "type": "event",
                "title": e.title,
                "slug": "",
                "cover_image": e.cover_image,
                "youtube_video_id": e.youtube_video_id,
            }
            for e in Event.objects.filter(is_published=True, show_in_gallery=True)
        ]
        payload = articles + events
        return Response(GalleryItemSerializer(payload, many=True).data)


class PreviewArticleView(APIView):
    permission_classes = [permissions.AllowAny]

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="token",
                required=True,
                location=OpenApiParameter.QUERY,
                description="Token HMAC assinado com expiração curta para preview",
                type=str,
            )
        ]
    )
    def get(self, request, slug: str):
        token = request.query_params.get("token", "")
        if not validate_preview_token(slug, token):
            return Response({"detail": "Token inválido"}, status=403)

        article = get_object_or_404(Article, slug=slug)
        return Response(ArticleSerializer(article).data)
