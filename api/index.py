"""Vercel serverless entry point.

Vercel's Python runtime looks for a module-level `app` (or `handler`) in this
file and drives it as a WSGI application.
"""
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fake_review_detector.settings')

from django.core.wsgi import get_wsgi_application  # noqa: E402

app = get_wsgi_application()
application = app
