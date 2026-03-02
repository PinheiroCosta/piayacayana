import hashlib
import hmac
import mimetypes
import re
import time
import unicodedata
from pathlib import Path
from urllib.parse import urlparse

from django.conf import settings
from django.core.exceptions import ValidationError

YOUTUBE_DOMAINS = {"youtube.com", "www.youtube.com", "youtu.be", "www.youtu.be"}


def extract_youtube_video_id(url: str) -> str:
    parsed = urlparse(url)
    if parsed.netloc.lower() not in YOUTUBE_DOMAINS:
        raise ValidationError("Domínio de YouTube inválido")

    if "youtu.be" in parsed.netloc.lower():
        video_id = parsed.path.strip("/")
    else:
        query = dict(item.split("=") for item in parsed.query.split("&") if "=" in item)
        video_id = query.get("v", "")

    if not re.fullmatch(r"[A-Za-z0-9_-]{11}", video_id):
        raise ValidationError("youtube_video_id inválido")
    return video_id


def sign_preview_token(slug: str, expires_in: int | None = None) -> str:
    ttl = expires_in or settings.PREVIEW_EXP_SECONDS
    exp = int(time.time()) + ttl
    payload = f"{slug}:{exp}"
    signature = hmac.new(settings.PREVIEW_SECRET.encode(), payload.encode(), hashlib.sha256).hexdigest()
    return f"{exp}.{signature}"


def validate_preview_token(slug: str, token: str) -> bool:
    try:
        exp_raw, signature = token.split(".", 1)
        exp = int(exp_raw)
    except ValueError:
        return False

    if exp < int(time.time()):
        return False

    payload = f"{slug}:{exp}"
    expected = hmac.new(settings.PREVIEW_SECRET.encode(), payload.encode(), hashlib.sha256).hexdigest()
    return hmac.compare_digest(signature, expected)


def sanitize_filename(filename: str) -> str:
    stem = Path(filename).stem
    suffix = Path(filename).suffix.lower()
    stem = unicodedata.normalize("NFKD", stem).encode("ascii", "ignore").decode("ascii")
    stem = re.sub(r"[^a-zA-Z0-9_-]", "-", stem).strip("-") or "arquivo"
    return f"{stem}{suffix}"


def validate_upload(file_obj) -> None:
    if file_obj.size > settings.MAX_UPLOAD_SIZE:
        raise ValidationError("Arquivo excede limite de tamanho")

    mime, _ = mimetypes.guess_type(file_obj.name)
    if mime is None:
        raise ValidationError("MIME type inválido")
