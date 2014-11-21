"""
Django settings for ProiezioniElezioni project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import socket
#from django.conf.global_settings import AUTH_USER_MODEL

BASE_DIR = os.path.dirname(os.path.dirname(__file__))



def contains(str, substr):
    if str.find(substr) != -1:
        return True
    else:
        return False

if contains(socket.gethostname(), 'webfaction'):
    LIVEHOST = True
else:
    LIVEHOST = False

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '71&)c_b1$_)1li9cdl)=24u#*mw(&f)_el=oowc^0wxf=uy506'

# SECURITY WARNING: don't run with debug turned on in production!

ADMINS = (
    ('Vincenzo Petrungaro', 'vincenzo.petrungaro@tiesi.it'),
)
MANAGERS = ADMINS

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    #'debug_toolbar.apps.DebugToolbarConfig',
    'bootstrapform',
    'elezioni',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    #'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.contrib.auth.backends.ModelBackend',
    #'django.middleware.transaction.TransactionMiddleware',
    #"django.core.context_processors.request",
)

from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS as TCP

TEMPLATE_CONTEXT_PROCESSORS = TCP + (
    'django.core.context_processors.request',
)

ROOT_URLCONF = 'proiezioni.urls'

WSGI_APPLICATION = 'proiezioni.wsgi.application'

LANGUAGE_CODE = 'it-IT'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

TIME_ZONE = 'Europe/Rome'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"),
)

SETTINGS_DIR = os.path.dirname(__file__)
PROJECT_PATH = os.path.join(SETTINGS_DIR, os.pardir)
PROJECT_PATH = os.path.abspath(PROJECT_PATH)

 # Absolute path to the media directory

LOGIN_REDIRECT_URL = '/'
LOGIN_URL = '/login/'
LOGOUT_URL = '/logout/'

if LIVEHOST:
    """
    Configurazione di Produzione
    """
    import secrets

    DEBUG = False
    TEMPLATE_DEBUG = False

    ALLOWED_HOSTS = []

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': secrets.DATABASE_NAME,
            'USER': secrets.DATABASE_USER,
            'PASSWORD': secrets.DATABASE_PASSWORD,
            'HOST': '',
            'PORT': '',
            'ATOMIC_REQUESTS': True,
        }
    }
    STATIC_URL = '/static/'
    STATIC_ROOT = '/home/tiesi/webapps/proiezioni_static/'
    MEDIA_URL = '/media/'
    MEDIA_ROOT = os.path.join(PROJECT_PATH, 'media')
else:
    """
    Configurazione di Sviluppo
    """
    DEBUG = True
    TEMPLATE_DEBUG = True

    ALLOWED_HOSTS = []

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
            'ATOMIC_REQUESTS': True,
        }
    }
    STATIC_URL = '/static/'
    MEDIA_URL = '/media/'
    MEDIA_ROOT = os.path.join(PROJECT_PATH, 'media')
    INSTALLED_APPS += ('debug_toolbar.apps.DebugToolbarConfig',)
    MIDDLEWARE_CLASSES += ('debug_toolbar.middleware.DebugToolbarMiddleware',)
