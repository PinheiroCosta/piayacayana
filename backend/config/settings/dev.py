from .base import *

try:
    from dotenv import load_dotenv
    load_dotenv(BASE_DIR / '.env')
except Exception:
    pass

DEBUG = True
CORS_ALLOWED_ORIGINS = CORS_ALLOWED_ORIGINS or ['http://localhost:3000']

SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False

DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'
