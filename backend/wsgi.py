"""
WSGI config for music_bingo project.
"""

import os
import logging

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'music_bingo.settings')

application = get_wsgi_application()

# Log all registered URLs after Django initialization
logger = logging.getLogger(__name__)
try:
    from django.urls import get_resolver
    resolver = get_resolver()
    logger.info("🔍 WSGI: Registered URL patterns after get_wsgi_application():")
    for pattern in resolver.url_patterns:
        logger.info(f"   - {pattern}")
        # If it's an include(), show nested patterns
        if hasattr(pattern, 'url_patterns'):
            for nested in pattern.url_patterns:
                logger.info(f"      └─ {nested}")
except Exception as e:
    logger.error(f"❌ Error listing URLs in WSGI: {e}")
