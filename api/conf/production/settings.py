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
Django rest framework cors headers """
# Allowing to render all requests to api from any domain
CORS_ORIGIN_ALLOW_ALL = True
CORS_URLS_REGEX = r'^/api/.*$'


"""
REST FRAMEWORK THROTTLING """
REST_FRAMEWORK.update({
    'DEFAULT_THROTTLE_CLASSES': (
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle',
    ),
    'DEFAULT_THROTTLE_RATES': {
        'anon': '100/day',
        'user': '5000/day',
    }
})

"""
Email settings use secure ssl connection """
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

EMAIL_HOST = os.getenv('EMAIL_HOST')
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')

EMAIL_USE_SSL = True
EMAIL_PORT = 465

EMAIL_SUBJECT_PREFIX = '[PmDragon] '
