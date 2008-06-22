import os.path


# Getting Started
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = BASE_DIR

# Debug Settings
DEBUG = True
TEMPLATE_DEBUG = DEBUG

# Basic Settings
TIME_ZONE = 'America/Los_Angeles'
LANGUAGE_CODE = 'en-us'

# Cache Settings
if DEBUG:
    CACHE_BACKEND = "dummy:///"
else:
    CACHE_BACKEND = "memcached://127.0.0.1:11211/"
    CACHE_MIDDLEWARE_SECONDS = 60 * 60
    CACHE_MIDDLEWARE_KEY_PREFIX = 'plugables'

# Site Settings
SITE_ID = 1
ROOT_URLCONF = 'urls'
USE_I18N = True

# Middleware
MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.middleware.http.SetRemoteAddrFromForwardedFor',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'applications.core.middleware.url.UrlMiddleware', # Custom Middleware
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.doc.XViewMiddleware',
    'django.middleware.http.ConditionalGetMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
)
USE_ETAGS = True
APPEND_SLASH = True
REMOVE_WWW = True


# Template Settings
MARKUP_FILTER = ('markdown', {})
TEMPLATE_DIRS = (
    os.path.join(os.path.dirname(__file__), 'templates'),
)
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
)

# Import Local Settings
try:
    from plugables import *
except ImportError:
    pass

