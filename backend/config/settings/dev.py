from dotenv import load_dotenv

from .base import *  # noqa: F403,F401

load_dotenv(BASE_DIR / ".env")  # noqa: F405
DEBUG = True
