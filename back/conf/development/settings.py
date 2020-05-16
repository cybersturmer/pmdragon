from conf.common.settings import *

DEBUG = True

ALLOWED_HOSTS = ['0.0.0.0', '127.0.0.1', 'localhost']

SECRET_KEY = 'w*ea%hd29u-&l&rol@5zo8a+@5o=@wb+i*r(@_+fnuc!*^9o0w'

ROOT_URLCONF = 'conf.development.urls'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')
MEDIA_URL = "/media/"

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}