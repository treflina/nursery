from os import getenv, path

from dotenv import load_dotenv

from .base import *  # noqa: F403

prod_env_file = path.join(BASE_DIR, ".envs", ".env.prod")

if path.isfile(prod_env_file):
    load_dotenv(prod_env_file)

DEBUG = False

STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

MIDDLEWARE = [*MIDDLEWARE, "whitenoise.middleware.WhiteNoiseMiddleware"]
if not TESTING:
    INSTALLED_APPS = [
        *INSTALLED_APPS,
        "debug_toolbar",
    ]
    MIDDLEWARE = [
        "debug_toolbar.middleware.DebugToolbarMiddleware",
        *MIDDLEWARE,
    ]

DATABASES = {
    "default": {
        "ENGINE": getenv("DB_ENGINE"),
        "NAME": getenv("DB_NAME"),
        "USER": getenv("DB_USER"),
        "PASSWORD": getenv("DB_PASSWORD"),
        "HOST": getenv("DB_HOST"),
        "PORT": getenv("DB_PORT"),
    }
}

SITE_NAME = getenv("SITE_NAME")

BASE_URL = getenv("BASE_URL")

SECRET_KEY = getenv("DJANGO_SECRET_KEY")

ALLOWED_HOSTS = getenv("ALLOWED_HOSTS").split()

ADMIN_URL = getenv("DJANGO_ADMIN_URL")

WEBPUSH_SETTINGS = {
    "VAPID_PUBLIC_KEY": getenv("VAPID_PUBLIC_KEY"),
    "VAPID_PRIVATE_KEY": getenv("VAPID_PRIVATE_KEY"),
    "VAPID_ADMIN_EMAIL": getenv("VAPID_ADMIN_EMAIL"),
}

if getenv("DEVIL"):
    STATIC_ROOT = path.join(BASE_DIR, "public", "static")
    MEDIA_ROOT = path.join(BASE_DIR, "public", "media")
else:
    STATIC_ROOT = path.join(BASE_DIR, "staticfiles")
    MEDIA_ROOT = path.join(BASE_DIR, "media")

# SECURITY
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#secure-proxy-ssl-header
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
# https://docs.djangoproject.com/en/dev/ref/settings/#secure-ssl-redirect
SECURE_SSL_REDIRECT = True
# https://docs.djangoproject.com/en/dev/ref/settings/#session-cookie-secure
SESSION_COOKIE_SECURE = True
# https://docs.djangoproject.com/en/dev/ref/settings/#session-cookie-name
SESSION_COOKIE_NAME = "__Secure-sessionid"
# https://docs.djangoproject.com/en/dev/ref/settings/#csrf-cookie-secure
CSRF_COOKIE_SECURE = True
# https://docs.djangoproject.com/en/dev/ref/settings/#csrf-cookie-name
CSRF_COOKIE_NAME = "__Secure-csrftoken"
