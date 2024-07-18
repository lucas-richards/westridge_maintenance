"""
Django settings for django_projects project.

Generated by 'django-admin startproject' using Django 4.1.7.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""
from dotenv import load_dotenv
from pathlib import Path
import os
import dj_database_url

# Load environment variables from .env
load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# SECRET_KEY = 'django-insecure-85!1hn^grnxz4ow*!b&)v=3f_v6ir$zz^*lxd3s@29i15mna($'

#Secret key generated with python
#SECRET_KEY = os.environ.get('SECRET_KEY')
SECRET_KEY = '123456'
EMAIL_USER="lucasrichardsdev@gmail.com"
EMAIL_PASS="kcuz qlta puhu mzwy"


# SECURITY WARNING: don't run with debug turned on in production!
#DEBUG = os.environ.get('DEBUG_VALUE')
DEBUG = True

ALLOWED_HOSTS = ['*','127.0.0.1','10.1.1.19',
                 'localhost',
                 'http://localhost:3000',
                 'westridgeapp.onrender.com']

CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
]


# Application definition

INSTALLED_APPS = [
    # 'rest_framework',
    'tasks.apps.TasksConfig',
    'training.apps.TrainingConfig',
    'users.apps.UsersConfig',
    'blog.apps.BlogConfig',
    'crispy_forms',
    'crispy_bootstrap4',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'storages',
    'corsheaders',
    
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'django_projects.urls'

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
                'blog.context_processors.all_users',
                'blog.context_processors.all_profiles',
            ],
        },
    },
]

# REST_FRAMEWORK = {
#     # Use Django's standard `django.contrib.auth` permissions,
#     # or allow read-only access for unauthenticated users.
#     'DEFAULT_PERMISSION_CLASSES': [
#         'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
#     ]
# }

WSGI_APPLICATION = 'django_projects.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

#db_from_env = dj_database_url.config(default='postgres://westridge_db_user:Uh6AA01PFj49hGHaDaiYqJlr2rThdapw@dpg-co4vsg4f7o1s739242r0-a.oregon-postgres.render.com/westridge_db')
# db_from_env = dj_database_url.config(default='postgres://house_o132_user:9QufcJHwj4oEveIOJGy1cEzFheAjVWWP@dpg-cmqs4amg1b2c73d808bg-a.oregon-postgres.render.com/house_o132')
# external                         connection postgres://house_o132_user:9QufcJHwj4oEveIOJGy1cEzFheAjVWWP@dpg-cmqs4amg1b2c73d808bg-a.oregon-postgres.render.com/house_o132

#DATABASES = {
#    'default': db_from_env
#}

DATABASES = {
     'default': {
         'ENGINE': 'django.db.backends.postgresql',
         'NAME': 'mydb',
         'USER': 'lucas',
         'PASSWORD': 'lucas',
         'HOST': 'localhost',
         'PORT': '5432',
     }
 }


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    # {
    #      'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    # },
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
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

# pacific time zone
TIME_ZONE = 'America/Los_Angeles'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
# This setting informs Django of the URI path from which your static files will be served to users
# Here, they well be accessible at your-domain.onrender.com/static/... or yourcustomdomain.com/static/...
STATIC_URL = '/static/'

# This production code might break development mode, so we check whether we're in DEBUG mode
if not DEBUG:
    # Tell Django to copy static assets into a path called `staticfiles` (this is specific to Render)
    STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
    # Enable the WhiteNoise storage backend, which compresses static files to reduce disk use
    # and renames the files with unique names for each version to support long-term caching
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

CRISPY_TEMPLATE_PACK = 'bootstrap4' 

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap4"

LOGIN_REDIRECT_URL = 'training-graph'
LOGIN_URL = 'get-code'

#variables to send email and reset password
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.environ.get('EMAIL_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_PASS')

#variables for AWS
AWS_ACCESS_KEY_ID=os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY=os.environ.get('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME=os.environ.get('AWS_STORAGE_BUCKET_NAME')

AWS_S3_FILE_OVERWRITE = False
AWS_DEFAULT_ACL = None

# uncomment this to turn on AWS storage
# DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

# django_heroku.settings(locals())
