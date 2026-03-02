from django.test import TestCase

from .utils import extract_youtube_video_id, sign_preview_token, validate_preview_token


class UtilsTests(TestCase):
    def test_extract_youtube_video_id(self):
        self.assertEqual(extract_youtube_video_id("https://youtu.be/dQw4w9WgXcQ"), "dQw4w9WgXcQ")

    def test_preview_token_roundtrip(self):
        slug = "post-teste"
        token = sign_preview_token(slug, expires_in=120)
        self.assertTrue(validate_preview_token(slug, token))
