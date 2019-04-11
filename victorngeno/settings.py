"""
Django settings for victorngeno project.

Generated by 'django-admin startproject' using Django 1.11.5.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

ALLOWED_HOSTS = ['localhost', 'veekay.herokuapp.com','victorngeno.com']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'blog',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # Simplified static file serving.
    # https://warehouse.python.org/project/whitenoise/
    'whitenoise.middleware.WhiteNoiseMiddleware',
]

ROOT_URLCONF = 'victorngeno.urls'

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

WSGI_APPLICATION = 'victorngeno.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases




# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, "static", "static_root")


STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static", "our_static"),
    # '/var/www/static/',
    )


MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, "static", "media_root")

# email settings
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'mailappvictor@gmail.com' #my gmail username
EMAIL_PORT = 587
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = "Victor <mailappvictor@gmail.com>"


ADMINS = [('Victor', EMAIL_HOST_USER)]
MANAGERS = ADMINS

try:
    from .local_settings import SECRET_KEY, DATABASES, EMAIL_HOST_PASSWORD
    #define local developments settings
    DEBUG = True
    SECRET_KEY = SECRET_KEY
    DATABASES = DATABASES
    EMAIL_HOST_PASSWORD = EMAIL_HOST_PASSWORD

except ImportError:
    #means the local_settings file is not deployed online
    #production settings are defined here
    DEBUG = False
    import dj_database_url
    from os import environ
    GEOS_LIBRARY_PATH = "{}/libgeos_c.so".format(environ.get('GEOS_LIBRARY_PATH'))
    GDAL_LIBRARY_PATH = "{}/libgdal.so".format(environ.get('GDAL_LIBRARY_PATH'))
    PROJ4_LIBRARY_PATH = "{}/libproj.so".format(environ.get('PROJ4_LIBRARY_PATH'))

    SECRET_KEY = os.environ.get('SECRET_KEY', '')
    db_from_env = dj_database_url.config()
    DATABASES = {'default': dj_database_url.config()}
    DATABASES['default']['ENGINE'] = 'django.contrib.gis.db.backends.postgis'

    EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')  # my gmail password
