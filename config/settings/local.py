from os import getenv, path

from dotenv import load_dotenv

from .base import *  # noqa
from .base import BASE_DIR

local_env_file = path.join(BASE_DIR, ".envs", ".env.local")

if path.isfile(local_env_file):
    load_dotenv(local_env_file)

DEBUG = True

SITE_NAME = getenv("SITE_NAME")

SECRET_KEY = getenv(
    "DJANGO_SECRET_KEY",
    "django-insecure-+zpoh9pvr1fo$^3e_u^yxr*$p5ebpmc4qgdkja9$y!j4@07gqv",
)

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

EMAIL_BACKEND = getenv(
    "DJANGO_EMAIL_BACKEND",
    default="django.core.mail.backends.console.EmailBackend",
)

# EMAIL_HOST = getenv("EMAIL_HOST")
# EMAIL_PORT = getenv("EMAIL_PORT")
# DEFAULT_FROM_EMAIL = getenv("DEFAULT_FROM_EMAIL")
# DOMAIN = getenv("DOMAIN")

INTERNAL_IPS = [
    "127.0.0.1",
]
