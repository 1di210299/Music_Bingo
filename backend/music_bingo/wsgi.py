"""
WSGI config for music_bingo project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os
import logging

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "music_bingo.settings")

application = get_wsgi_application()

# Log all registered URLs at startup to verify karaoke endpoints are loaded
logger = logging.getLogger(__name__)
try:
    from django.urls import get_resolver
    resolver = get_resolver()
    url_patterns = [str(pattern) for pattern in resolver.url_patterns]
    logger.info("=" * 80)
    logger.info("🔍 WSGI STARTUP - Registered URL patterns:")
    for pattern in url_patterns:
        logger.info(f"   {pattern}")
    
    # Check specifically for karaoke URLs
    from api import urls as api_urls
    karaoke_urls = [str(p) for p in api_urls.urlpatterns if 'karaoke' in str(p)]
    logger.info("=" * 80)
    logger.info("🎤 KARAOKE URLs in api/urls.py:")
    for url in karaoke_urls:
        logger.info(f"   {url}")
    logger.info("=" * 80)
except Exception as e:
    logger.error(f"❌ Error logging URLs: {e}")
