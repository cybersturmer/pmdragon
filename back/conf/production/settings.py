from conf.common.settings import *

DEBUG = False

ALLOWED_HOSTS = [os.getenv('DJANGO_ALLOWED_HOSTS')]

SECRET_KEY = os.getenv('DJANGO_SECRET_KEY')
assert SECRET_KEY is not None, (
    'Please provide DJANGO_SECRET_KEY env variable with a value'
)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('POSTGRES_DB'),
        'USER': os.getenv('POSTGRES_USER'),
        'PASSWORD': os.getenv('POSTGRES_PASSWORD'),
        'HOST': os.getenv('POSTGRES_HOST'),
        'PORT': '5432',
    }
}

ROOT_URLCONF = 'conf.production.urls'

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': 'memcached:11211',
        'TIMEOUT': os.getenv('DJANGO_CACHE_TIMEOUT')
    }
}

"""
Email settings """
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

EMAIL_HOST = 'smtp.yandex.ru'
EMAIL_HOST_USER = 'cybersturmer@ya.ru'

EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')

EMAIL_PORT = 25
EMAIL_SUBJECT_PREFIX = '[PmDragon] '
