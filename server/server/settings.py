"""
Django settings for server project.

Generated by 'django-admin startproject' using Django 3.2.4.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""
from pathlib import Path
from django.utils.translation import gettext_lazy as _
import os
# Build paths inside the project like this: BASE_DIR / 'subdir'.
from django.contrib.messages import constants as messages
import server
from decouple import config
BASE_DIR = Path(__file__).resolve().parent.parent
from django.conf.locale.ru import formats as ru_formats



# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY')
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG')

ALLOWED_HOSTS = ['*']

BASE_URL = config('BASE_URL')

TOKEN = config('TOKEN')

LISTEN_WEBHOOK = config('LISTEN_WEBHOOK')

WEBHOOK_PORT = config('WEBHOOK_PORT')

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # lib apps
    'django_tgbot',
    'rest_framework',
    'behave_django',
    'markdownx',
    # custom apps,
    'accounts',
    'KitchenWeb',
    'psycopg2',
    'global_user',

]

MIDDLEWARE = [
    'accounts.middlewares.auth.CustomAuthMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'server.urls'

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

WSGI_APPLICATION = 'server.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': config('DB_NAME', ''),
        'HOST': config('DB_HOST'),
        'PORT': config('DB_PORT'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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

LANGUAGES = [
    ('en', _('English')),
    ('ru', _('Russian')),
]

# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/


LANGUAGE_CODE = 'ru-RU'
TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = False

USE_TZ = True

ru_formats.DATE_FORMAT = 'd.m.Y'

ru_formats.TIME_FORMAT = 'H:i'

ru_formats.DATETIME_FORMAT = 'd.m.Y H:i'

DATE_FORMAT = 'j E Y'

TIME_FORMAT = 'H:i'

DATETIME_FORMAT = 'j E Y H:i'
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'

MEDIA_URL = '/uploads/'

STATIC_ROOT = os.path.join(BASE_DIR, 'static')

MEDIA_ROOT = os.path.join(BASE_DIR, 'uploads')

LOCALE_PATHS = [
    os.path.join(BASE_DIR, 'locale')
]



# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

MESSAGE_TAGS = {
    messages.ERROR: 'danger',
    messages.SUCCESS: 'success',
}



TEMPLATES[0]['OPTIONS']['context_processors'].append("global_user.templatetags.context_processors.check_admin")
TEMPLATES[0]['OPTIONS']['context_processors'].append("global_user.templatetags.context_processors.offering_in_cart")