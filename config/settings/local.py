from .base import *



DEBUG = True
# dev-specific overrides 


# Local DB (SQLite by default for dev)
DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }


# Use local-memory cache for development and tests to avoid needing Redis locally.
# This prevents tests from failing if Redis is not running.
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "dev-cache",
    }
}


# Use in-memory channel layer for Channels (prevents channels_redis connection attempts)
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels.layers.InMemoryChannelLayer",
    },
}


REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": 
        ("rest_framework_simplejwt.authentication.JWTAuthentication",)
}