from .base import *


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-d77o6*^80uw6^k78vc2a)w+8f)r_y14suq$f4ja7%tx61^pf_4"

DEBUG = True
ALLOWED_HOSTS = []


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

WSGI_APPLICATION = "core.wsgi.application"


STATICFILES_DIRS = [
    BASE_DIR / 'static',
]
MEDIA_ROOT = BASE_DIR / 'uploaded_media'

