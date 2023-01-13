"""
Django settings for myEnrollment project.

Generated by 'django-admin startproject' using Django 4.1.4.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""

from pathlib import Path
import os
from datetime import timedelta

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG= os.environ.get('DJANGO_DEBUG') == 'True'

if os.environ.get('DJANGO_ALLOWED_HOSTS'):
    ALLOWED_HOSTS = os.environ.get('DJANGO_ALLOWED_HOSTS').split(',')

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'corsheaders',
    'teachersAuth',
    'rest_framework_simplejwt',
    'secondarySchools',
    # "mail"
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
]

ROOT_URLCONF = 'myEnrollment.urls'

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

WSGI_APPLICATION = 'myEnrollment.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases
"""
GITHUB_WORKFLOW env is only available in github actions.
On server other non-GITHUB env var will be used from repository secret
"""
if os.getenv('GITHUB_WORKFLOW'):
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': os.environ.get('DATABASE_NAME'), # we could use other GITHUB_secrets
            'USER': os.environ['DATABASE_USER'],
            'PASSWORD':os.environ['DATABASE_PASS'],
            'TEST': {
                'NAME': os.environ.get('DATABASE_TEST_NAME')
            }
            # 'HOST': os.environ['GITHUB_DB_HOST']
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': os.environ.get('DATABASE_NAME'),
            'USER': os.environ.get('DATABASE_USER'),
            'PASSWORD':os.environ.get('DATABASE_PASS'),
            'TEST': {
                'NAME': os.environ.get('DATABASE_TEST_NAME')
            }
        }
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

# PASSWORD_HASHERS = [
#     'django.contrib.auth.hashers.PBKDF2PasswordHasher',
#     'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
#     'django.contrib.auth.hashers.Argon2PasswordHasher',
#     'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
#     'django.contrib.auth.hashers.ScryptPasswordHasher',
# ]

# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Europe/Sarajevo'

USE_I18N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static/')

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
AUTH_USER_MODEL= 'teachersAuth.Teacher'
JWT_PRIVATE_KEY= os.environ.get('JWT_PRIVATE_KEY')
# to allow all frontend ports to access app
CORS_ORIGIN_ALLOW_ALL= True
"""
we login with cookies and return the cookie,
if not set, our frontend will not be able to see the cookies
"""
CORS_ALLOW_CREDENTIALS= True

REST_FRAMEWORK = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=30),
    "NON_FIELD_ERRORS_KEY": "errors",
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
        "rest_framework.authentication.SessionAuthentication",
        "rest_framework.authentication.TokenAuthentication",
        #'rest_framework_simplejwt.authentication.JWTTokenUserAuthentication'
        #'rest_framework.authentication.SessionAuthentication',
        #'rest_framework.authentication.BasicAuthentication',
    ),
    "DEFAULT_PERMISSION_CLASSES": (
        "rest_framework.permissions.IsAuthenticated",
        'rest_framework.permissions.IsAdminUser',
        ),
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 3,
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(hours=2),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
    "SIGNING_KEY": SECRET_KEY,
    "AUTH_HEADER_TYPES": ("JWT","Bearer"),
    # "Bearer <Token>"
}
# JWTStatelessUserAuthentication
# JWTTokenUserAuthentication
# https://django-rest-framework-simplejwt.readthedocs.io/en/latest/stateless_user_authentication.html#jwtstatelessuserauthentication-backend

DEFAULT_FROM_EMAIL= os.environ.get('DEFAULT_FROM_EMAIL')
SENDGRID_API_KEY = os.getenv('SENDGRID_API_KEY')
EMAIL_HOST = os.environ.get('EMAIL_HOST')
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER') # django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST_PASSWORD = SENDGRID_API_KEY
EMAIL_PORT = 587 # or 25 for TLS (unencrypted), 465 for SSL
EMAIL_USE_TLS = True
EMAIL_BACKEND = "sendgrid_backend.SendgridBackend"
# https://simpleit.rocks/python/django/adding-email-to-django-the-easiest-way/
# Toggle sandbox mode (when running in DEBUG mode)
SENDGRID_SANDBOX_MODE_IN_DEBUG=False

# echo to stdout or any other file-like object that is passed to the backend via the stream kwarg.
#SENDGRID_ECHO_TO_STDOUT=True
