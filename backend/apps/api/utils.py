import hashlib
import hmac
import time

from django.conf import settings


def generate_preview_token(kind: str, slug: str) -> str:
    expires = int(time.time()) + settings.PREVIEW_TOKEN_TTL_SECONDS
    payload = f'{kind}:{slug}:{expires}'
    signature = hmac.new(settings.PREVIEW_TOKEN_SECRET.encode(), payload.encode(), hashlib.sha256).hexdigest()
    return f'{expires}.{signature}'


def validate_preview_token(kind: str, slug: str, token: str) -> bool:
    if not token or '.' not in token:
        return False
    expires_str, signature = token.split('.', 1)
    if not expires_str.isdigit() or int(expires_str) < int(time.time()):
        return False
    payload = f'{kind}:{slug}:{expires_str}'
    expected = hmac.new(settings.PREVIEW_TOKEN_SECRET.encode(), payload.encode(), hashlib.sha256).hexdigest()
    return hmac.compare_digest(signature, expected)
