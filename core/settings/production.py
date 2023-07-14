from .base import *

" It's randomly created by 'get_random_secret_key' "
SECRET_KEY = '61+w32#45-^m2!8j18$$9cya=77@mndtdsb+m_$0-s(+kungi*'

DEBUG = False
ALLOWED_HOSTS = [
    'example.com',
    'www.example.com',
    'subdomain.example.com',
    '10.0.0.1',
    '10.0.0.2',
    '192.168.1.1',
    '192.168.1.2',
    '172.16.0.1',
    '172.16.0.2',
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'fake_db_name',
        'USER': 'fake_db_user',
        'PASSWORD': 'fake_db_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'youremail@gmail.com'
EMAIL_HOST_PASSWORD = 'yourpassword'


WSGI_APPLICATION = "core.wsgi.application"


