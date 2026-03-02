from django.urls import path

from .views import (
    PreviewArticleView,
    PublicArticleDetailView,
    PublicArticleListView,
    PublicEventListView,
    PublicGalleryView,
    PublicPageDetailView,
)

urlpatterns = [
    path('public/pages/<slug:slug>/', PublicPageDetailView.as_view()),
    path('public/articles/', PublicArticleListView.as_view()),
    path('public/articles/<slug:slug>/', PublicArticleDetailView.as_view()),
    path('public/events/', PublicEventListView.as_view()),
    path('public/gallery/', PublicGalleryView.as_view()),
    path('preview/articles/<slug:slug>/', PreviewArticleView.as_view()),
]
