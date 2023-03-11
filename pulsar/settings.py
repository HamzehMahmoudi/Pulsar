"""
Django settings for pulsar project.

Generated by 'django-admin startproject' using Django 4.1.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""

from pathlib import Path
import os
from dotenv import load_dotenv
from datetime import timedelta
load_dotenv()
env = os.getenv

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY')
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'daphne',
    'django.contrib.staticfiles',
    # libraries
    'rest_framework',
    'rest_framework_simplejwt',
    'channels',
    'corsheaders',
    'crispy_forms',
    'azbankgateways',

    # apps
    'chat',
    'accounts',
    'payment'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    "corsheaders.middleware.CorsMiddleware",
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
CORS_ALLOW_ALL_ORIGINS = True
ROOT_URLCONF = 'pulsar.urls'

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

WSGI_APPLICATION = 'pulsar.wsgi.application'
ASGI_APPLICATION = 'pulsar.asgi.application'

# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        "NAME": os.getenv('POSTGRES_DB'),
        "USER": os.getenv('POSTGRES_USER'),
        "PASSWORD": os.getenv('POSTGRES_PASSWORD'),
        "HOST": os.getenv('DB_HOST'),
        'Options': {
            'collation': 'utf8mb4_unicode_ci',
        }
    }
}
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [(env('REDIS_HOST', 'localhost'), 6379)],
        },
    },
}
REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 10

}
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=10),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=20),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': False,
    'UPDATE_LAST_LOGIN': False,

    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'VERIFYING_KEY': None,
    'AUDIENCE': None,
    'ISSUER': None,
    'JWK_URL': None,
    'LEEWAY': 0,

    'AUTH_HEADER_TYPES': ('Bearer',),
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
    'USER_AUTHENTICATION_RULE': 'rest_framework_simplejwt.authentication.default_user_authentication_rule',

    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',
    'TOKEN_USER_CLASS': 'rest_framework_simplejwt.models.TokenUser',

    'JTI_CLAIM': 'jti',

    'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',
    'SLIDING_TOKEN_LIFETIME': timedelta(days=10),
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=20),
}
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

AZ_IRANIAN_BANK_GATEWAYS = {
   'GATEWAYS': {
       'BMI': {
           'MERCHANT_CODE': '<YOUR MERCHANT CODE>',
           'TERMINAL_CODE': '<YOUR TERMINAL CODE>',
           'SECRET_KEY': '<YOUR SECRET CODE>',
       },
       'SEP': {
           'MERCHANT_CODE': '<YOUR MERCHANT CODE>',
           'TERMINAL_CODE': '<YOUR TERMINAL CODE>',
       },
       'ZARINPAL': {
           'MERCHANT_CODE': '<YOUR MERCHANT CODE>',
           'SANDBOX': 0,  # 0 disable, 1 active
       },
       'IDPAY': {
           'MERCHANT_CODE': '779cfe4c-d13a-4b1e-a107-2d72af39e20c',
           'METHOD': 'POST',
           'X_SANDBOX': 1, 
       },
       'ZIBAL': {
           'MERCHANT_CODE': '<YOUR MERCHANT CODE>',
       },
       'BAHAMTA': {
           'MERCHANT_CODE': '<YOUR MERCHANT CODE>',
       },
       'MELLAT': {
           'TERMINAL_CODE': '<YOUR TERMINAL CODE>',
           'USERNAME': '<YOUR USERNAME>',
           'PASSWORD': '<YOUR PASSWORD>',
       },
       'PAYV1': {
           'MERCHANT_CODE': '<YOUR MERCHANT CODE>',
           'X_SANDBOX': 0,
       },
   },
   'IS_SAMPLE_FORM_ENABLE': True,
   'DEFAULT': 'IDPAY',
   'CURRENCY': 'IRT',
   'TRACKING_CODE_QUERY_PARAM': 'tc', 
   'TRACKING_CODE_LENGTH': 16, 
   'SETTING_VALUE_READER_CLASS': 'azbankgateways.readers.DefaultReader', 
   'BANK_PRIORITIES': [
       'IDPAY',
       'BMI',
       'SEP',
   ],
}

# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = "/static/"
STATICFILES_DIRS = (
        os.path.join(BASE_DIR, 'static'),
)
# STATICFILES_DIRs = [ 
MEDIA_ROOT = BASE_DIR / 'media/'
MEDIA_URL = "/media/"


# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field
AUTH_USER_MODEL = 'accounts.User'
CRISPY_TEMPLATE_PACK = "bootstrap4"
LOGIN_REDIRECT_URL = "index"
LOGIN_URL = "login"
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
