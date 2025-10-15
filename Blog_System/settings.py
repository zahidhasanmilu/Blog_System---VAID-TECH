
from pathlib import Path
import os


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-r3nw=@^cx@15s8*png_#kb(saqi2i=lop9)nbc^f#z6-243#mb'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []
# DEBUG = False
# ALLOWED_HOSTS = ['*'] 



# -----------------------------
# Default Django apps
# -----------------------------
INSTALLED_APPS = [
    'django.contrib.admin',          # Admin panel
    'django.contrib.auth',           # Authentication system
    'django.contrib.contenttypes',   # Content types framework
    'django.contrib.sessions',       # Session framework
    'django.contrib.messages',       # Messaging framework
    'django.contrib.staticfiles',    # Static file handling
    'ckeditor',                      # CKEditor for rich text editing
    'ckeditor_uploader',  
     'crispy_forms',
    'crispy_bootstrap4',
    
    'rest_framework',                # Django REST framework
]
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap4"
CRISPY_TEMPLATE_PACK = "bootstrap4"
# -----------------------------
# Custom apps
# -----------------------------
CUSTOM_APPS = [
    'app_account.apps.AppAccountConfig',   # Custom user & profile app
    'app_home',                            # Blog/homepage app
    'django_cleanup.apps.CleanupConfig',   # Automatically delete old files
    'app_home_api.apps.AppHomeApiConfig',  # API for the blog app
]

# Combine default and custom apps
INSTALLED_APPS += CUSTOM_APPS

AUTH_USER_MODEL = 'app_account.CustomUser'



MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    
    'app_home.middlewares.UnderConstructionMiddleware',  # Custom middleware
    "app_account.middlewares.ResendMailMiddleware",
    
]

ROOT_URLCONF = 'Blog_System.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                
                # my custom context processors
                'app_home.context_processors.get_all_categories',
                'app_home.context_processors.get_all_tags',
                'app_home.context_processors.get_recent_blogs',
            ],
        },
    },
]

WSGI_APPLICATION = 'Blog_System.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Dhaka'

USE_I18N = True

USE_TZ = True



# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/
STATIC_URL = '/static/'
STATIC_ROOT = 'staticfiles'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static')
]

MEDIA_URL='/media/'
MEDIA_ROOT=os.path.join(BASE_DIR ,'media')


# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'



# CKEditor upload path
CKEDITOR_UPLOAD_PATH = "uploads/"



#-----------------Email Settings-----------------
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = "zahidhasan.miluu@gmail.com"
EMAIL_HOST_PASSWORD = "supa fdic chnn hent"


# Celery Configuration Options
CELERY_BROKER_URL = 'redis://localhost:6379/0'          # Task Queue
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'      # Task Result
CELERY_TIMEZONE = 'Asia/Dhaka'


