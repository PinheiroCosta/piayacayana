from django.core.exceptions import ValidationError
from django.db import models

from .utils import extract_youtube_video_id, sanitize_filename, validate_upload


class TimestampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Page(models.Model):
    title = models.CharField(max_length=150)
    slug = models.SlugField(unique=True)
    content = models.TextField()
    is_published = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.title


class Article(TimestampedModel):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    summary = models.TextField()
    content = models.TextField()
    cover_image = models.URLField(blank=True)
    youtube_url = models.URLField(blank=True, null=True)
    youtube_video_id = models.CharField(max_length=11, blank=True)
    show_in_gallery = models.BooleanField(default=False)
    is_published = models.BooleanField(default=False)
    published_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        ordering = ["-published_at", "-created_at"]

    def clean(self) -> None:
        if self.youtube_url:
            self.youtube_video_id = extract_youtube_video_id(self.youtube_url)

    def __str__(self) -> str:
        return self.title


class Event(TimestampedModel):
    title = models.CharField(max_length=200)
    description = models.TextField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    location = models.CharField(max_length=255)
    cover_image = models.URLField(blank=True)
    youtube_url = models.URLField(blank=True, null=True)
    youtube_video_id = models.CharField(max_length=11, blank=True)
    show_in_gallery = models.BooleanField(default=False)
    is_published = models.BooleanField(default=False)

    class Meta:
        ordering = ["start_date"]

    def clean(self) -> None:
        if self.end_date < self.start_date:
            raise ValidationError("end_date deve ser maior ou igual ao start_date")
        if self.youtube_url:
            self.youtube_video_id = extract_youtube_video_id(self.youtube_url)

    def __str__(self) -> str:
        return self.title


def media_upload_to(instance, filename: str) -> str:
    return f"media/{sanitize_filename(filename)}"


class Media(models.Model):
    IMAGE = "image"
    VIDEO = "video"
    TYPE_CHOICES = ((IMAGE, "Imagem"), (VIDEO, "Vídeo"))

    file = models.FileField(upload_to=media_upload_to)
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    related_article = models.ForeignKey(Article, on_delete=models.SET_NULL, null=True, blank=True)
    related_event = models.ForeignKey(Event, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self) -> None:
        validate_upload(self.file)

    def __str__(self) -> str:
        return f"{self.type} - {self.pk}"
