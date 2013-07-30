from os.path import join,  dirname,  normpath

PROJECT_ROOT = join(dirname(normpath(__file__)), '..')
DEBUG = False
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('Han Mdarien', 'han.mdarien@gmail.com'),
)

MANAGERS = ADMINS

DATABASE_ENGINE = ''           # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
DATABASE_NAME = ''             # Or path to database file if using sqlite3.
DATABASE_USER = ''             # Not used with sqlite3.
DATABASE_PASSWORD = ''         # Not used with sqlite3.
DATABASE_HOST = ''             # Set to empty string for localhost. Not used with sqlite3.
DATABASE_PORT = ''             # Set to empty string for default. Not used with sqlite3.

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'UTC'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"

APPEND_SLASH = True

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
STATIC_ROOT = join(PROJECT_ROOT, 'static')
STATIC_URL = '/static/'
MEDIA_ROOT = join(PROJECT_ROOT,  'media')
MEDIA_URL = '/media/'
STATIC_LOCAL_ROOT = join(PROJECT_ROOT, 'static_local')
STATIC_LOCAL_URL = '/static_local/'


# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/static/admin_media/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = '34#wzfbj^rcz+s_s7g95j9f#6ykabcbxp^4dp!i)1!ajnt5%o!'
INTERNAL_ACCESS_KEY = '7IUnmHjVZgCIDBY06_fABQZZ'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
#    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.Loader',   
# 'django.template.loaders.app_directories.load_template_source',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

ROOT_URLCONF = 'project.urls'

TEMPLATE_DIRS = (
    join(PROJECT_ROOT,  'templates/'), 
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth', 
    'django_defaultcontext.context_processors.defaults',
    'django.core.context_processors.debug', 
    'django.core.context_processors.i18n', 
    'django_community.context_processors.community',
)

INSTALLED_APPS = (
    'django.contrib.admin', 
    'django.contrib.sites',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.markup', 
    'south',
    'info',
    'django_extensions',
    'django_defaultcontext',
    'django_utils',
    'django_tracking',
    'tagging',
    'django_ec2',
    'django_rds',
    'django_community',
    'core',
)

PROJECT_APPS = (
    'core',
)

AUTHENTICATION_BACKENDS = ('django.contrib.auth.backends.ModelBackend',)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'file':{
            'level':'INFO',
            'class':'logging.FileHandler',
            'filename':'%s/test.log' % (PROJECT_ROOT),
            'formatter': 'simple'
        },
        'queries': {
            'level':'DEBUG',
            'class':'logging.FileHandler',
            'filename':'%s/queries.log' % (PROJECT_ROOT),
            'formatter': 'simple',
        },
        'console':{
            'level':'INFO',
            'class':'logging.StreamHandler',
            'formatter': 'simple'
        },
    },
    'loggers': {
        'django.db.backends': {
            'handlers':['queries', 'file', 'console'],
            'propagate': False,
            'level':'DEBUG',
        },
        'django': {
            'handlers':['file', 'console'],
            'propagate': True,
            'level':'INFO',
        },
    }
}

PRIMARY_SERVER = True

HOST_URL = ''
