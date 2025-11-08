from datetime import timedelta
from pathlib import Path
import os

# E402 ত্রুটি দূর করতে এটি উপরে আনা হয়েছে
from celery.schedules import crontab


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-r3nw=@^cx@15s8*png_#kb(saqi2i=lop9)nbc^f#z6-243#mb"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# ALLOWED_HOSTS = ['hypnoidal-raeann-shaggily.ngrok-free.dev']
ALLOWED_HOSTS = []
# DEBUG = False
# ALLOWED_HOSTS = ['*']


# -----------------------------
# Default Django apps
# -----------------------------
INSTALLED_APPS = [
    "account.apps.AccountConfig",
    "django.contrib.admin",  # Admin panel
    "django.contrib.auth",  # Authentication system
    "django.contrib.contenttypes",  # Content types framework
    "django.contrib.sessions",  # Session framework
    "django.contrib.messages",  # Messaging framework
    "django.contrib.staticfiles",  # Static file handling
    "django_extensions",
    "ckeditor",  # CKEditor for rich text editing
    "ckeditor_uploader",
    "crispy_forms",
    "crispy_bootstrap4",
    "rest_framework",  # Django REST framework
    "rest_framework.authtoken",  # Token authentication
    "rest_framework_simplejwt",  # JWT authentication
    "django_filters",  # Filtering support for DRF
    "drf_yasg",  # Swagger
]
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap4"
CRISPY_TEMPLATE_PACK = "bootstrap4"
# -----------------------------
# Custom apps
# -----------------------------
CUSTOM_APPS = [
    "blog",  # Blog/homepage app
    # E501 ফিক্সড
    "django_cleanup.apps.CleanupConfig",  # Automatically delete old files
    "blog_api.apps.AppHomeApiConfig",  # API for the blog app
]

# Combine default and custom apps
INSTALLED_APPS += CUSTOM_APPS

AUTH_USER_MODEL = "app_account.CustomUser"


MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "blog.middlewares.UnderConstructionMiddleware",  # Custom middleware
    "account.middlewares.ResendMailMiddleware",  # Custom middleware
]

ROOT_URLCONF = "blog_site.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": ["templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                # my custom context processors
                "blog.context_processors.get_all_categories",
                "blog.context_processors.get_all_tags",
                "blog.context_processors.get_recent_blogs",
            ],
        },
    },
]

WSGI_APPLICATION = "blog_site.wsgi.application"


# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        # E501 ফিক্সড
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "Asia/Dhaka"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/
STATIC_URL = "/static/"
STATIC_ROOT = "staticfiles"
STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")


# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# CKEditor upload path
CKEDITOR_UPLOAD_PATH = "uploads/"


# -----------------Email Settings-----------------
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = "zahidhasan.miluu@gmail.com"
EMAIL_HOST_PASSWORD = "supa fdic chnn hent"


# -----------------Celery Configuration Options-----------------
CELERY_BROKER_URL = "redis://localhost:6379/0"  # Task Queue
CELERY_RESULT_BACKEND = "redis://localhost:6379/0"  # Task Result
CELERY_TIMEZONE = "Asia/Dhaka"
CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TASK_SERIALIZER = "json"

# Django REST Framework Configuration
# https://www.django-rest-framework.org/api-guide/settings/
# Global permission settings
REST_FRAMEWORK = {
    # Global authentication settings
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.SessionAuthentication",  # Browser login/logout
        # 'rest_framework.authentication.BasicAuthentication', # Postman simple auth
        # 'rest_framework.authentication.TokenAuthentication', # Token based API
        # E501 ফিক্সড
        "rest_framework_simplejwt.authentication.JWTAuthentication",  # JWT based API
    ],
    # Global permission settings
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
    # Global throttle settings
    "DEFAULT_THROTTLE_CLASSES": [
        # Throttle for anonymous users
        "rest_framework.throttling.AnonRateThrottle",
        # Throttle for authenticated users
        "rest_framework.throttling.UserRateThrottle",
    ],
    "DEFAULT_THROTTLE_RATES": {
        "anon": "500/hour",  # Anonymous user 5 req/hour (E501 ফিক্সড)
        "user": "10/minute",  # Authenticated user 10 req/minute (E501 ফিক্সড)
    },
    # Global filter settings
    "DEFAULT_FILTER_BACKENDS": [
        "django_filters.rest_framework.DjangoFilterBackend",
        "rest_framework.filters.SearchFilter",
        "rest_framework.filters.OrderingFilter",
    ],
    "ORDERING_PARAM": "ordered_by",  # Default ordering parameter
    "SEARCH_PARAM": "search_by",  # Default search parameter
    # Global pagination settings
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 2,  # প্রতি পৃষ্ঠায় আইটেমের সংখ্যা
}

# ------------------  start JWT Configuration    ------------------#

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=2),  # short token life
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),  # longer refresh life
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
}

# ------------------  end JWT Configuration    ------------------#


# -------------------START CELERY_BEAT_SCHEDULE------------------- #

CELERY_BEAT_SCHEDULE = {
    "send-engagement-email-every-2-minutes": {
        "task": "account.tasks.send_engagement_email_to_all_users",
        "schedule": crontab(minute="*/2"),  # every 2 minutes
    },
    "print-time-every-day": {
        "task": "account.tasks.print_current_time",
        "schedule": crontab(hour=23, minute=59),  # every day at 11:59 PM
    },
}

# ------------------  end CELERY_BEAT_SCHEDULE    ------------------#


# ------------------  start logggin    ------------------#
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "standard": {
            "format": "{levelname} {asctime} {module} {process:d} {thread:d} {message}",
            "style": "{",
        },
        "simple": {
            "format": "{levelname} {message}",
            "style": "{",
        },
    },
    "handlers": {
        "console": {
            "level": "INFO",
            "class": "logging.StreamHandler",
            "formatter": "simple",
        },
        "file": {
            "level": "ERROR",
            "class": "logging.FileHandler",
            "filename": BASE_DIR / "log/debug.log",
            "formatter": "standard",
        },
        "rotating_file": {
            "level": "ERROR",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": BASE_DIR / "log/rotating_debug.log",
            "formatter": "standard",
            "maxBytes": 1024 * 1024 * 5,  # 5 MB
            "backupCount": 3,
        },
        "timed_rotating_file": {
            "level": "ERROR",
            "class": "logging.handlers.TimedRotatingFileHandler",
            "filename": BASE_DIR / "log/timed_debug.log",
            "formatter": "standard",
            "when": "midnight",
            "interval": 1,
            "backupCount": 3,
        },
    },
    "loggers": {
        "": {
            "handlers": ["console"],
            "propagate": True,
        },
        "create_blog": {
            "handlers": ["rotating_file", "timed_rotating_file"],
            "level": "DEBUG", 
            "propagate": False,
        },
    },
}
# ------------------   end logggin    ------------------#

# ---- Sentry ---

import sentry_sdk

sentry_sdk.init(
    dsn="https://cdd31fc8a813aa27b405d1025f458183@o4510329327386624.ingest.de.sentry.io/4510329400787024",
    # Add data like request headers and IP for users,
    # see https://docs.sentry.io/platforms/python/data-management/data-collected/ for more info
    send_default_pii=True,
)