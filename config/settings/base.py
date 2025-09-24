from pathlib import Path
import dj_database_url
import environ
import os



ROOT_DIR = Path(__file__).resolve().parent.parent.parent
env = environ.Env()
# read .env at project root if present
env.read_env(str(ROOT_DIR / ".env"))


BASE_DIR = ROOT_DIR


# SECURITY WARNING: keep the secret key secret!
SECRET_KEY = env("SECRET_KEY", default="django-insecure-j=#l70v6@vtc+05j8vexl^b@j8untf%4_=%z)^q7=ab=gg9l&!")


# Debug setting
DEBUG = env.bool("DEBUG", default=False)


# Allowed hosts
ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=["127.0.0.1", "localhost"])


INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # 3rd party
    "graphene_django",
    "django_filters",
    "channels",
    "channels_redis",
    "django_redis",
    "rest_framework",
    "rest_framework.authtoken",
    "rest_framework_simplejwt",
    "graphql_jwt.refresh_token.apps.RefreshTokenConfig",
    "whitenoise.runserver_nostatic",
    
    # local apps
    "users.apps.UsersConfig",
    'posts.apps.PostsConfig',
    "interactions.apps.InteractionsConfig",
]


MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware", # for serving static files in production
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]


# URL configuration
ROOT_URLCONF = "config.urls"


# Templates (basic)
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {"context_processors": [
            "django.template.context_processors.debug",
            "django.template.context_processors.request",
            "django.contrib.auth.context_processors.auth",
            "django.contrib.messages.context_processors.messages",
        ]},
    }
]


WSGI_APPLICATION = "config.wsgi.application"
ASGI_APPLICATION = "config.asgi.application"


# Default database (can be overridden in local.py / production.py)
DATABASES = {
    "default": dj_database_url.config(
        default=os.environ.get("postgresql://postgres:pFIsYZUnixmvdXVwsDloQaHWPtffQKVS@postgres.railway.internal:5432/railway")
    )
}


# Password validation (keep defaults)
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",},
]


# Internationalization
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True


# Static and media files
STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")

# Media files (user uploads)
MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")


DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# Graphene
GRAPHENE = {
    "SCHEMA": "config.schema.schema",
    "MIDDLEWARE": [
        "graphql_jwt.middleware.JSONWebTokenMiddleware",
    ],
}


# Authentication backends (including JWT)
AUTHENTICATION_BACKENDS = [
    "graphql_jwt.backends.JSONWebTokenBackend",
    "django.contrib.auth.backends.ModelBackend",
]


# Channels / Redis
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {"hosts": [env("REDIS_URL", default="redis://redis:6379/0")]},
    }
}


# Custom user if you intend to use one later:
AUTH_USER_MODEL = "users.User"


# Redis cache
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://localhost:6379/1",  # change if using Docker
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        },
        "KEY_PREFIX": "social_feed",
    }
}


# Django REST Framework
REST_FRAMEWORK = {
    "DEFAULT_THROTTLE_CLASSES": [
        "rest_framework.throttling.UserRateThrottle",
    ],
    "DEFAULT_THROTTLE_RATES": {
        "user": "1000/day"
    }
}


# Logging (basic console)
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {"console": {"class": "logging.StreamHandler"}},
    "root": {"handlers": ["console"], "level": "WARNING"},
}


# Static files storage with WhiteNoise
STORAGES = {
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    }
}