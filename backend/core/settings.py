import os
import logging.config
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(BASE_DIR / '.env')

SERVICE_NAME = os.getenv("K_SERVICE")

SECRET_KEY = os.getenv("SECRET_KEY")

DEBUG = os.getenv("DEBUG") == "True"

MAINTENANCE_MODE = os.getenv("MAINTENANCE_MODE") == "True"

ALLOWED_HOSTS = [
    'ervelus-web-service-324377414272.us-central1.run.app',
    'ervelus-generations-service-324377414272.us-central1.run.app',
    'localhost',
    '127.0.0.1'
]



INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'corsheaders',
    'gdpr_assist',
    'django_otp',
    'django_otp.plugins.otp_totp',
    'solo',

    'rest_framework',
    'rest_framework.authtoken',

    'core',
    'users',
    'products',
    'payments',
    'generations',
    'agreements',
    'marketing',
    'telegram_bot'
]



MIDDLEWARE = [
    'core.middleware.MaintenanceModeMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django_otp.middleware.OTPMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware'
]



ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages'
            ],
        },
    },
]

ASGI_APPLICATION = 'core.asgi.application'

WEB_WORKER_URL = os.getenv("WEB_WORKER_URL")
GENERATIONS_WORKER_URL = os.getenv("GENERATIONS_WORKER_URL")
BACKGROUND_WORKER_URL = os.getenv("BACKGROUND_WORKER_URL")



REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
    )
}



SESSION_ENGINE = 'django.contrib.sessions.backends.signed_cookies'
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SECURE = not DEBUG
SESSION_COOKIE_SAMESITE = 'None'



CSRF_TRUSTED_ORIGINS = [
    'https://ervelus-web-service-324377414272.us-central1.run.app',
    'http://localhost:5173',
    'http://127.0.0.1:5173'
]
CSRF_COOKIE_HTTPONLY = True
CSRF_COOKIE_SECURE = not DEBUG
CSRF_COOKIE_SAMESITE = 'None'



CORS_ALLOWED_ORIGINS = [
    'https://ervelus.com',
    'https://tma.ervelus.com',
    'https://credible-cosine-479914-k2.web.app',
    'https://credible-cosine-479914-k2.firebaseapp.com',
    'http://localhost:5173',
    'http://127.0.0.1:5173'
]
CORS_ALLOW_CREDENTIALS = True



GCP_PROJECT_ID = os.getenv("GCP_PROJECT_ID")
GCP_TASKS_LOCATION = os.getenv("GCP_TASKS_LOCATION")
GCP_TASKS_GENERATION_EVENTS_QUEUE_ID = os.getenv("GCP_TASKS_GENERATION_EVENTS_QUEUE_ID")
GCP_TASKS_RESIZE_EVENTS_QUEUE_ID = os.getenv("GCP_TASKS_RESIZE_EVENTS_QUEUE_ID")
GCP_TASKS_DELETE_EVENTS_QUEUE_ID = os.getenv("GCP_TASKS_DELETE_EVENTS_QUEUE_ID")
GCP_COMPLIANCE_BUCKET_NAME = os.getenv("GCP_COMPLIANCE_BUCKET_NAME")
GCP_STORAGE_BUCKET_NAME = os.getenv("GCP_STORAGE_BUCKET_NAME")
GCP_TEMP_BUCKET_NAME = os.getenv("GCP_TEMP_BUCKET_NAME")



TELEGRAM_API_KEY = os.getenv("TELEGRAM_API_KEY")
TELEGRAM_WEBHOOK_SECRET = os.getenv("TELEGRAM_WEBHOOK_SECRET")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")



DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'postgres',
        'USER': 'postgres',
        'PASSWORD': os.getenv("DB_PASSWORD"),
        'HOST': os.getenv("DB_HOST"),
        'PORT': '5432'
    }
}



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
    }
]



if DEBUG:
    active_handlers = ["file"]
else:
    active_handlers = ["google_cloud_handler"]

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "google_json_formatter": {
            "()": "pythonjsonlogger.jsonlogger.JsonFormatter",
            "format": "%(message)s",
        }
    },
    "handlers": {
        "file": {
            "class": "logging.FileHandler",
            "filename": BASE_DIR / "debug.log"
        },
        "google_cloud_handler": {
            "class": "google.cloud.logging.handlers.StructuredLogHandler",
            "formatter": "google_json_formatter"
        },
        "null": {
            "class": "logging.NullHandler",
        }
    },
    "loggers": {
        "django.request": {
            "handlers": active_handlers,
            "level": "ERROR",
            "propagate": False,
        },
        "httpx": {
            "handlers": active_handlers,
            "level": "ERROR",
            "propagate": False,
        },
        "google_genai": {
            "handlers": active_handlers,
            "level": "WARNING",
            "propagate": False
        }
    },
    "root": {
        "handlers": active_handlers,
        "level": "INFO",
    }
}

logging.config.dictConfig(LOGGING)



LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Europe/Kyiv'

USE_I18N = True

USE_TZ = True

STATIC_URL = 'static/'

STATIC_ROOT = BASE_DIR / 'staticfiles'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

GDPR_LOG_ON_ANONYMISE = False