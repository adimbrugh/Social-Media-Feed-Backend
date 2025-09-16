from .base import *

DEBUG = False
ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=["yourdomain.com"])
# add security settings:
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
# update DB/Cache if needed via environment
# e.g. DATABASE_URL, CACHE_URL