"""
Django settings for store project.

Generated by 'django-admin startproject' using Django 4.2.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""
import environ
import os.path
import socket
from pathlib import Path


env = environ.Env(
    # set casting, default value
    DEBUG=(bool, False),
    SECRET_KEY=(str),
    DOMAIN_NAME=(str),

    DATABASE_NAME=(str),
    DATABASE_USER=(str),
    DATABASE_PASSWORD=(str),
    DATABASE_HOST=(str),
    DATABASE_PORT=(str),

    REDIS_HOST=(str),
    REDIS_PORT=(str),

    EMAIL_HOST=(str),
    EMAIL_PORT=(str),
    EMAIL_HOST_USER=(str),
    EMAIL_HOST_PASSWORD=(str),
    EMAIL_USE_TLS=(bool),
    EMAIL_USE_SSL=(bool),

    STRIPE_PUBLICK_KEY=(str),
    STRIPE_SECRET_KEY=(str),
    STRIPE_WEBHOOK_SECRET_KEY=(str)
)

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Подгружаем данные с файла .env
environ.Env.read_env(BASE_DIR / '.env')

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env('DEBUG')

ALLOWED_HOSTS = ['127.0.0.1', 'localhost', 'web-app']

# Глобальная переменная, созданная собственноручно, для слияния с ссылкой отправки письма подтверждения
DOMAIN_NAME = env('DOMAIN_NAME')

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',  # Конвертирует числа в денежную форму

    "debug_toolbar",
    "django_extensions",
    
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.github',

    'products',
    'users',
    'orders',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    "allauth.account.middleware.AccountMiddleware",
    "debug_toolbar.middleware.DebugToolbarMiddleware",
]

ROOT_URLCONF = 'store.urls'

# DEBUG_TOOLBAR

INTERNAL_IPS = [
    '127.0.0.1',
    'localhost'
]


hostname, _, ips = socket.gethostbyname_ex(socket.gethostname())
INTERNAL_IPS += [".".join(ip.split(".")[:-1] + ["1"]) for ip in ips]

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
                'products.context_processors.baskets'
            ],
        },
    },
]

WSGI_APPLICATION = 'store.wsgi.application'

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'HOST': env('DATABASE_HOST'),
        'NAME': env('DATABASE_NAME'),
        'USER': env('DATABASE_USER'),
        'PASSWORD': env('DATABASE_PASSWORD'),
        'PORT': env('DATABASE_PORT')
    }
}

# REDIS

REDIS_HOST = env('REDIS_HOST')
REDIS_PORT = env('REDIS_PORT')

# CACHE
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": f"redis://{REDIS_HOST}:{REDIS_PORT}",
        "OPTIONS": {
            "db": "1",
            "pool_class": "redis.BlockingConnectionPool",
        },
    }
}

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'ru'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Users

AUTH_USER_MODEL = 'users.User'  # Глобально переопределяем модель с которой мы работаем
LOGIN_URL = 'users:index'  # Глобальная переменная(ссылка), для декоратора login_required, для переадресации
LOGIN_REDIRECT_URL = 'index'  # Глобальная переменная, для переадресации при авторизации
LOGOUT_REDIRECT_URL = 'index'  # Глобальная переменная, для переадресации при logout

# Sending email
if DEBUG:
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
else:
    EMAIL_HOST = env('EMAIL_HOST')
    EMAIL_PORT = env('EMAIL_PORT')
    EMAIL_HOST_USER = env('EMAIL_HOST_USER')
    EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD')
    EMAIL_USE_TLS = env('EMAIL_USE_TLS')
    EMAIL_USE_SSL = env('EMAIL_USE_SSL')

# Settings django-allauth

SITE_ID = 1

AUTHENTICATION_BACKENDS = [
    # Needed to log in by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',
    # `allauth` specific authentication methods, such as login by email
    'allauth.account.auth_backends.AuthenticationBackend',
]

# Provider specific settings
SOCIALACCOUNT_PROVIDERS = {
    'github': {
        'SCOPE': [
            'user',
            'repo',
            'read:org',
        ],
    }
}

# CELERY

CELERY_BROKER_URL = f'redis://{REDIS_HOST}:{REDIS_PORT}/0'
CELERY_RESULT_BACKEND = f'redis://{REDIS_HOST}:{REDIS_PORT}/0'


# STRIPE 
STRIPE_PUBLIC_KEY = env('STRIPE_PUBLIC_KEY')
STRIPE_SECRET_KEY = env('STRIPE_SECRET_KEY')
STRIPE_WEBHOOK_SECRET_KEY = env('STRIPE_WEBHOOK_SECRET_KEY')
