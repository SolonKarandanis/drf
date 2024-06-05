"""
Django settings for cfehome project.

Generated by 'django-admin startproject' using Django 4.1.7.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""
import datetime
import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-o)zsmn*_u6^f*^v7+lzpyoqgt%q+=38jjzp!o3g$n%8nzhv)26'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = [
    "daphne",
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.postgres',
    'django_crontab',
    'corsheaders',
    'rest_framework',
    'rest_framework.authtoken',
    "debug_toolbar",
    "django_celery_results",
    'django_celery_beat',
    'channels',
    'auth',
    'products',
    'cart',
    'orders',
    'mail',
    'notifications',
    'chat',
    'comments',
    'images',
    'socials'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    "debug_toolbar.middleware.DebugToolbarMiddleware"
]

ROOT_URLCONF = 'cfehome.urls'
CORS_URLS_REGEX = r"^/api/.*"
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOWED_ORIGINS = [
    'http://localhost:3000'
]

# if DEBUG:
#     CORS_ALLOWED_ORIGINS += [
#         'http://localhost:3000',
#     ]

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

WSGI_APPLICATION = 'cfehome.wsgi.application'
ASGI_APPLICATION = 'cfehome.asgi.application'

# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'drf',
        'USER': 'drf',
        'PASSWORD': 'drf',
        'HOST': '192.168.1.5',
        'PORT': '5432'
    }
}

# CONN_MAX_AGE = 60
# CONN_HEALTH_CHECKS = True

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        }
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
        },
        'file': {
            'class': 'logging.FileHandler',
            'filename': 'logs/drf.log',
            'level': 'DEBUG',
        }
    },
    'loggers': {
        'django.db.backends': {
            'level': 'DEBUG',
            'handlers': ['console'],
        }
    }
}

# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/
from django.utils.translation import gettext_lazy as _

LANGUAGE_CODE = 'en'

LANGUAGES = (
    ('en', _('en')),
    ('fr', _('fr')),
)

LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'locale/'),
)

TIME_ZONE = 'Europe/Athens'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
AUTH_USER_MODEL = 'custom_auth.User'

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.AllowAny"
    ],
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.LimitOffsetPagination",
    "PAGE_SIZE": 10
}

SIMPLE_JWT = {
    "AUTH_HEADER_TYPES": ["Bearer"],
    "ACCESS_TOKEN_LIFETIME": datetime.timedelta(hours=3),
}
INTERNAL_IPS = [
    "127.0.0.1",
]

# REDIS_URL = 'redis://192.168.1.5:6379/0'

# Celery Settings
CELERY_BROKER_URL = ''
accept_content = ['application/json']
result_serializer = 'json'
task_serializer = 'json'
CELERY_TIMEZONE = 'Europe/Athens'
CELERY_ENABLE_UTC = False
CELERY_RESULT_BACKEND = 'redis://192.168.1.5:6379/0'
CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers:DatabaseScheduler'

# SMTP
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_USE_TLS = True
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_HOST_USER = "skarandanis@gmail.com"
EMAIL_HOST_PASSWORD = ""
DEFAULT_FROM_EMAIL = "Testing <>"

# CHANNEL_LAYERS = {
#     'default': {
#         'BACKEND': 'channels_redis.core.RedisChannelLayer',
#         'CONFIG': {
#             "hosts": [('192.168.1.5', 6379)],
#         },
#     },
# }

# CACHES = {
#     'default': {
#         'BACKEND': 'django_redis.cache.RedisCache',
#         'LOCATION': REDIS_URL,
#         'OPTIONS': {
#             'CLIENT_CLASS': 'django_redis.client.DefaultClient',
#             "SOCKET_CONNECT_TIMEOUT": 5,  # seconds
#             "SOCKET_TIMEOUT": 5,  # seconds
#             "COMPRESSOR": "django_redis.compressors.zlib.ZlibCompressor",
#             "IGNORE_EXCEPTIONS": True,
#         },
#         "KEY_PREFIX": "drf"
#     }
# }

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

AMQP_URL = 'amqp://guest:guest@localhost/%2f'

BANNED_IPS = []

LOG_FILE =os.path.join(BASE_DIR, 'logs/'),
CRONJOBS = [
    ('0 0 * * *', 'cfehome.cron.remove_unverified_users', f'>> {LOG_FILE}/cron_jobs.log'),
]