# Add rest_framework and related apps to INSTALLED_APPS
INSTALLED_APPS = [
    ...
    'rest_framework',
    'django_filters',               # Add django-filters
    'rest_framework_simplejwt',
    'messaging_app.chats',          # Ensure your app is included
]

# DRF configuration
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',  # optional, for web
        'rest_framework.authentication.BasicAuthentication',    # optional, for testing
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'messaging_app.chats.permissions.IsParticipantOfConversation',
    ),
    'DEFAULT_PAGINATION_CLASS': 'messaging_app.chats.pagination.MessagePagination',
    'PAGE_SIZE': 20,
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
    ),
}

# Simple JWT settings (optional: adjust expiry)
from datetime import timedelta

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'AUTH_HEADER_TYPES': ('Bearer',),
}
