import os
import re
import unicodedata
from urllib.parse import parse_qs, urlparse

from django.core.exceptions import ValidationError
from django.core.files.storage import default_storage
from django.utils.crypto import get_random_string

ALLOWED_YOUTUBE_HOSTS = {'youtube.com', 'www.youtube.com', 'youtu.be', 'www.youtu.be'}
YOUTUBE_ID_RE = re.compile(r'^[A-Za-z0-9_-]{11}$')


def extract_youtube_video_id(url: str | None) -> str | None:
    if not url:
        return None
    parsed = urlparse(url)
    if parsed.netloc not in ALLOWED_YOUTUBE_HOSTS:
        raise ValidationError('URL do YouTube inválida.')

    if 'youtu.be' in parsed.netloc:
        video_id = parsed.path.strip('/').split('/')[0]
    else:
        qs = parse_qs(parsed.query)
        video_id = qs.get('v', [''])[0]
        if not video_id and parsed.path.startswith('/embed/'):
            video_id = parsed.path.split('/embed/')[-1].split('/')[0]

    if not YOUTUBE_ID_RE.match(video_id):
        raise ValidationError('ID de vídeo do YouTube inválido.')
    return video_id


def sanitize_filename(filename: str) -> str:
    name, ext = os.path.splitext(filename)
    normalized = unicodedata.normalize('NFKD', name).encode('ascii', 'ignore').decode('ascii')
    normalized = re.sub(r'[^a-zA-Z0-9_-]+', '-', normalized).strip('-').lower() or 'arquivo'
    return f"{normalized}-{get_random_string(6).lower()}{ext.lower()}"


def public_file_url(file_field) -> str:
    if not file_field:
        return ''
    if default_storage.exists(file_field.name):
        return default_storage.url(file_field.name)
    return ''
