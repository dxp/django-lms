from common import *

DEBUG = True
TEMPLATE_DEBUG = DEBUG

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django_mongodb_engine', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'intranet_test',                      # Or path to database file if using sqlite3.
    }
}

COMPRESS_ENABLED = True
COMPRESS_REBUILD_TIMEOUT = 1

CELERY_ALWAYS_EAGER = True

INSTALLED_APPS.append('devserver')
