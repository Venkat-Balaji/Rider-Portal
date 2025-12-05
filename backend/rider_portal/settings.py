import os
from pathlib import Path
import environ

BASE_DIR = Path(__file__).resolve().parent.parent
env = environ.Env(DEBUG=(bool, False))
environ.Env.read_env(os.path.join(BASE_DIR, '.env')) if os.path.exists(os.path.join(BASE_DIR, '.env')) else None

SECRET_KEY = env('DJANGO_SECRET_KEY', default='change-me')
DEBUG = env.bool('DEBUG', default=True)
ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=['127.0.0.1', 'localhost'])

INSTALLED_APPS = [
    'django.contrib.admin', 'django.contrib.auth', 'django.contrib.contenttypes',
    'django.contrib.sessions', 'django.contrib.messages', 'django.contrib.staticfiles',
    'rest_framework', 'drf_spectacular',
    'users', 'qr', 'documents', 'audits', 'notifications',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
]

ROOT_URLCONF = 'rider_portal.urls'

# rider_portal/settings.py (update the TEMPLATES section)
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # Add the project-level templates directory:
        'DIRS': [ BASE_DIR / 'templates' ],
        'APP_DIRS': True,
        'OPTIONS': {'context_processors': [
            'django.template.context_processors.debug',
            'django.template.context_processors.request',
            'django.contrib.auth.context_processors.auth',
            'django.contrib.messages.context_processors.messages',
        ]},
    },
]


WSGI_APPLICATION = 'rider_portal.wsgi.application'

# DB: default sqlite for ease. Override with DATABASE_URL env var for Postgres.
DATABASES = {
    'default': env.db('DATABASE_URL', default='sqlite:///' + str(BASE_DIR / 'db.sqlite3'))
}

AUTH_USER_MODEL = 'users.User'  # custom user model defined below

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_TZ = True
STATIC_URL = '/static/'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rider_portal_auth.SupabaseAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.CursorPagination',
    'PAGE_SIZE': 20,
}

SPECTACULAR_SETTINGS = {
    'TITLE': 'RideSafe Rider Portal API',
    'VERSION': '1.0.0',
}

# Supabase config
SUPABASE_JWKS_URL = env('SUPABASE_JWKS_URL', default='')
SUPABASE_AUDIENCE = env('SUPABASE_AUDIENCE', default=None)
SUPABASE_ISS = env('SUPABASE_ISS', default=None)
SUPABASE_SERVICE_KEY = env('SUPABASE_SERVICE_KEY', default=None)
SUPABASE_STORAGE_BUCKET = env('SUPABASE_STORAGE_BUCKET', default='public')
