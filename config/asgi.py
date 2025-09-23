"""
ASGI config for config project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/asgi/
"""

from channels.routing import ProtocolTypeRouter, URLRouter
from interactions.middleware import TokenAuthMiddleware
from django.core.asgi import get_asgi_application
import interactions.routing
import django
import os



# Auto-detect environment
if os.environ.get("DJANGO_ENV") == "production":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.production")
    django.setup()
else:
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.local")
    django.setup()
    
    
# Standard Django ASGI application
django_asgi_app = get_asgi_application()
    
    
application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": TokenAuthMiddleware(
        URLRouter(
            interactions.routing.websocket_urlpatterns
        )
    ),
})
    