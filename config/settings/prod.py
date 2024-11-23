from os import getenv, path

from dotenv import load_dotenv

from .base import *  # noqa: F403

prod_env_file = path.join(BASE_DIR, ".envs", ".env.prod")

if path.isfile(prod_env_file):
    load_dotenv(prod_env_file)

DEBUG = False
TESTING = False

STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

MIDDLEWARE = [*MIDDLEWARE, "whitenoise.middleware.WhiteNoiseMiddleware"]

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

SECRET_KEY = getenv("DJANGO_SECRET_KEY")

ALLOWED_HOSTS = getenv("ALLOWED_HOSTS").split()

if not TESTING:
    INSTALLED_APPS = [
        *INSTALLED_APPS,
        "debug_toolbar",
    ]
    MIDDLEWARE = [
        "debug_toolbar.middleware.DebugToolbarMiddleware",
        *MIDDLEWARE,
    ]

ADMIN_URL = getenv("DJANGO_ADMIN_URL")
