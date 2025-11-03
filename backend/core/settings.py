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
    'ervelus-web-service-281870812434.us-central1.run.app',
    'ervelus-web-service-7miwsuv5aa-uc.a.run.app',
    'backend.ervelus.com',
    'localhost',
    '127.0.0.1'
]



INSTALLED_APPS = [
    'django.contrib.sites',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'gdpr_assist',
    'django_otp',
    'django_otp.plugins.otp_totp',
    'auditlog',
    'anymail',
    'solo',

    'rest_framework',

    'dj_rest_auth',
    'dj_rest_auth.registration',

    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',

    'core',
    'users',
    'products',
    'subscriptions',
    'generations',
    'agreements'
]

SITE_ID = 1



AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

ACCOUNT_ADAPTER = 'users.adapters.CustomAccountAdapter'
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'
ACCOUNT_EMAIL_SUBJECT_PREFIX = "Welcome to Ervelus! "
ACCOUNT_RATE_LIMITS = {
    'confirm_email': '1/15s',
}



SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'APP': {
            'client_id': os.getenv('GOOGLE_CLIENT_ID'),
            'secret': os.getenv('GOOGLE_CLIENT_SECRET'),
        },
        'SCOPE': [
            'email',
        ],
    }
}

SOCIALACCOUNT_EMAIL_VERIFICATION = 'mandatory'
SOCIALACCOUNT_AUTO_SIGNUP = True
SOCIALACCOUNT_EMAIL_AUTHENTICATION = True
SOCIALACCOUNT_EMAIL_AUTHENTICATION_AUTO_CONNECT	= True
SOCIALACCOUNT_ADAPTER = 'users.adapters.CustomSocialAccountAdapter'



MIDDLEWARE = [
    'core.middleware.MaintenanceModeMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django_otp.middleware.OTPMiddleware',
    'allauth.account.middleware.AccountMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'auditlog.middleware.AuditlogMiddleware'
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
                'django.contrib.messages.context_processors.messages',
                'core.context_processors.frontend_url',
            ],
        },
    },
]

ASGI_APPLICATION = 'core.asgi.application'

WEB_WORKER_URL = os.getenv("WEB_WORKER_URL")
GENERATIONS_WORKER_URL = os.getenv("GENERATIONS_WORKER_URL")
BACKGROUND_WORKER_URL = os.getenv("BACKGROUND_WORKER_URL")
FRONTEND_URL = os.getenv("FRONTEND_URL")



REST_AUTH = {
    'TOKEN_MODEL': None,
    'REGISTER_SERIALIZER': 'users.serializers.CustomRegisterSerializer',
    'LOGIN_SERIALIZER': 'users.serializers.CustomLoginSerializer'
}

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
    ),
    'DEFAULT_THROTTLE_CLASSES': (
        'core.throttling.CustomScopedRateThrottle',
    ),
    'DEFAULT_THROTTLE_RATES': {
        'auth_anon': '5/minute',
        'contact_anon': '5/hour'
    }
}



SESSION_ENGINE = 'django.contrib.sessions.backends.signed_cookies'
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SECURE = not DEBUG
SESSION_COOKIE_SAMESITE = 'Lax'
SESSION_COOKIE_AGE = 3888000



CSRF_TRUSTED_ORIGINS = [
    'https://ervelus.com',
    'https://backend.ervelus.com',
    'https://valiant-hexagon-471121-i7.web.app',
    'http://localhost:5173',
    'http://127.0.0.1:5173'
]
CSRF_COOKIE_HTTPONLY = False
CSRF_COOKIE_SECURE = not DEBUG
CSRF_COOKIE_SAMESITE = 'Lax'



ANYMAIL = {
    "MAILGUN_API_KEY": os.getenv("MAILGUN_API_KEY"),
    "MAILGUN_SENDER_DOMAIN": os.getenv("MAILGUN_SENDER_DOMAIN"),
    "MAILGUN_API_URL": os.getenv("MAILGUN_API_BASE_URL")
}

MAILGUN_API_KEY = os.getenv("MAILGUN_API_KEY")
MAILGUN_SENDER_DOMAIN = os.getenv("MAILGUN_SENDER_DOMAIN")
MAILGUN_API_BASE_URL = os.getenv("MAILGUN_API_BASE_URL")
MAILGUN_MAILING_LIST_ADDRESS = os.getenv("MAILGUN_MAILING_LIST_ADDRESS")

EMAIL_BACKEND = "anymail.backends.mailgun.EmailBackend"
DEFAULT_FROM_EMAIL = os.getenv("DEFAULT_FROM_EMAIL")



PADDLE_API_KEY = os.getenv("PADDLE_API_KEY")
PADDLE_API_BASE_URL = os.getenv("PADDLE_API_BASE_URL")
PADDLE_WEBHOOK_SECRET_KEY = os.getenv("PADDLE_WEBHOOK_SECRET_KEY")



GCP_PROJECT_ID = os.getenv("GCP_PROJECT_ID")
GCP_TASKS_SECRET_KEY = os.getenv("GCP_TASKS_SECRET_KEY")
GCP_TASKS_LOCATION = os.getenv("GCP_TASKS_LOCATION")
GCP_TASKS_PADDLE_EVENTS_QUEUE_ID = os.getenv("GCP_TASKS_PADDLE_EVENTS_QUEUE_ID")
GCP_TASKS_GENERATION_EVENTS_QUEUE_ID = os.getenv("GCP_TASKS_GENERATION_EVENTS_QUEUE_ID")
GCP_TASKS_RESIZE_EVENTS_QUEUE_ID = os.getenv("GCP_TASKS_RESIZE_EVENTS_QUEUE_ID")
GCP_TASKS_DELETE_EVENTS_QUEUE_ID = os.getenv("GCP_TASKS_DELETE_EVENTS_QUEUE_ID")
GCP_STORAGE_BUCKET_NAME = os.getenv("GCP_STORAGE_BUCKET_NAME")
GCP_TEMP_BUCKET_NAME = os.getenv("GCP_TEMP_BUCKET_NAME")



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
    "handlers": {
        "file": {
            "class": "logging.FileHandler",
            "filename": BASE_DIR / "debug.log"
        },
        "google_cloud_handler": {
            "class": "google.cloud.logging.handlers.CloudLoggingHandler",
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
        "paddle_billing": {
            "handlers": ["null"],
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

AUDITLOG_INCLUDE_ALL_MODELS = True

AUDITLOG_EXCLUDE_TRACKING_MODELS = (
    "generations.GenerationRequest",
)

GDPR_LOG_ON_ANONYMISE = False