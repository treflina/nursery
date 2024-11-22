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

DATABASES = {
    'default': {
        'ENGINE': getenv("DB_ENGINE"),
        'NAME': getenv("DB_NAME"),
        'USER': getenv("DB_USER"),
        'PASSWORD': getenv("DB_PASSWORD"),
        'HOST': getenv("DB_HOST"),
        'PORT': getenv("DB_PORT")
    }
}