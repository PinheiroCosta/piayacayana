from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone

from .utils import extract_youtube_video_id, sanitize_filename


class BaseTimestampModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class PublishableModel(models.Model):
    is_published = models.BooleanField(default=False)

    class Meta:
        abstract = True


class Page(PublishableModel):
    title = models.CharField(max_length=160)
    slug = models.SlugField(unique=True)
    content = models.TextField()
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Article(BaseTimestampModel, PublishableModel):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    summary = models.TextField()
    content = models.TextField()
    cover_image = models.URLField(blank=True)
    youtube_url = models.URLField(blank=True)
    youtube_video_id = models.CharField(max_length=11, blank=True)
    show_in_gallery = models.BooleanField(default=False)
    published_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-published_at', '-created_at']

    def clean(self):
        self.youtube_video_id = extract_youtube_video_id(self.youtube_url)
        if self.is_published and not self.published_at:
            self.published_at = timezone.now()

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Event(PublishableModel):
    title = models.CharField(max_length=200)
    description = models.TextField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    location = models.CharField(max_length=255)
    cover_image = models.URLField(blank=True)
    youtube_url = models.URLField(blank=True)
    youtube_video_id = models.CharField(max_length=11, blank=True)
    show_in_gallery = models.BooleanField(default=False)

    class Meta:
        ordering = ['start_date']

    def clean(self):
        if self.end_date < self.start_date:
            raise ValidationError('Data de término não pode ser anterior à data de início.')
        self.youtube_video_id = extract_youtube_video_id(self.youtube_url)

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Media(BaseTimestampModel):
    TYPE_IMAGE = 'image'
    TYPE_VIDEO = 'video'
    TYPE_CHOICES = ((TYPE_IMAGE, 'Imagem'), (TYPE_VIDEO, 'Vídeo'))

    file = models.FileField(upload_to='uploads/%Y/%m/')
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    related_article = models.ForeignKey(Article, on_delete=models.SET_NULL, null=True, blank=True)
    related_event = models.ForeignKey(Event, on_delete=models.SET_NULL, null=True, blank=True)
    public_url = models.URLField(blank=True)

    class Meta:
        verbose_name_plural = 'media'

    def clean(self):
        uploaded_file = self.file
        if uploaded_file and uploaded_file.size > settings.MAX_UPLOAD_SIZE:
            raise ValidationError('Arquivo excede tamanho permitido.')
        content_type = getattr(uploaded_file, 'content_type', '')
        if content_type and content_type not in settings.ALLOWED_UPLOAD_MIME_TYPES:
            raise ValidationError('Tipo MIME não permitido.')
        if uploaded_file:
            uploaded_file.name = sanitize_filename(uploaded_file.name)

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
        file_url = self.file.url if self.file else ''
        if file_url and self.public_url != file_url:
            self.public_url = file_url
            super().save(update_fields=['public_url'])

    def __str__(self):
        return self.file.name
