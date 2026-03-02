from .base import *  # noqa: F403,F401

import os

DEBUG = False
SECURE_SSL_REDIRECT = True
SECURE_HSTS_SECONDS = 3600
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

frontend_url = os.getenv("DJANGO_FRONTEND_URL", "")
CORS_ALLOWED_ORIGINS = [frontend_url] if frontend_url else []
