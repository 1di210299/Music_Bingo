"""
WSGI config for music_bingo project.
"""

import os
import logging

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'music_bingo.settings')

application = get_wsgi_application()

# ⚡ CRITICAL FIX FOR COLD STARTS ⚡
# Force Django to preload URL patterns and views BEFORE first request
# Without this, Django lazy-loads on first request (50+ second delay)
# See: https://simon-ninon.medium.com/making-django-deployments-less-disruptive-5ace190f6d8e
logger = logging.getLogger(__name__)
try:
    from django.urls import get_resolver
    resolver = get_resolver()
    # THIS LINE IS CRITICAL: Forces import of all urls.py + views + models
    _ = resolver.url_patterns
    logger.info(f"✅ WSGI: Preloaded {len(resolver.url_patterns)} URL patterns successfully")
except Exception as e:
    logger.error(f"❌ Error preloading URLs in WSGI: {e}")
