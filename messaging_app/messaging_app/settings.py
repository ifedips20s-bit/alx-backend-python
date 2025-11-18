# Add rest_framework to INSTALLED_APPS if not already present
INSTALLED_APPS = [
    ...
    'rest_framework',
    'rest_framework_simplejwt',
    'messaging_app.chats',  # Ensure your app is included
]

# DRF default authentication
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',  # optional, for web
        'rest_framework.authentication.BasicAuthentication',    # added
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    )
}

# Simple JWT settings (optional: adjust expiry)
from datetime import timedelta

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'AUTH_HEADER_TYPES': ('Bearer',),
}
