"""
Django settings for messaging_app project.
"""

from pathlib import Path
from datetime import timedelta
from dotenv import load_dotenv
import os
load_dotenv()


BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'replace-this-with-your-own-secret-key'
DEBUG = True

ALLOWED_HOSTS = []


# -------------------------
# INSTALLED_APPS
# -------------------------
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third-party apps
    'rest_framework',
    'django_filters',
    'rest_framework_simplejwt',

    # Local apps
    'chats',
]


# -------------------------
# MIDDLEWARE
# -------------------------
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'chats.middleware.RequestLoggingMiddleware',        # log every request
    'chats.middleware.RestrictAccessByTimeMiddleware',  # restrict access by time
]


# -------------------------
# URLS & TEMPLATES
# -------------------------
ROOT_URLCONF = 'messaging_app.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'messaging_app.wsgi.application'


# -------------------------
# DATABASE
# -------------------------
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# -------------------------
# PASSWORD VALIDATION
# -------------------------
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# -------------------------
# INTERNATIONALIZATION
# -------------------------
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True


# -------------------------
# STATIC FILES
# -------------------------
STATIC_URL = 'static/'


# -------------------------
# DEFAULT PRIMARY KEY
# -------------------------
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'



# ============================================================
#                DJANGO REST FRAMEWORK CONFIG
# ============================================================
REST_FRAMEWORK = {

    # --- Authentication classes ---
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',  # browser login
        'rest_framework.authentication.BasicAuthentication',    # Postman basic auth
    ),

    # --- Global permissions ---
    'DEFAULT_PERMISSION_CLASSES': (
        'chats.permissions.IsParticipantOfConversation',
    ),

    # --- Pagination ---
    'DEFAULT_PAGINATION_CLASS': 'chats.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,

    # --- Filtering ---
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
    ),
}



# ============================================================
#                      SIMPLE JWT SETTINGS
# ============================================================
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'AUTH_HEADER_TYPES': ('Bearer',),
}
AUTH_USER_MODEL = 'chats.User'
